import scrapy
from ..items import KactorItem  # your Scrapy item
import random
import re
from datetime import datetime

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_2_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) Gecko/20100101 Firefox/124.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
]
AJAX_HEADERS = {
    "User-Agent": random.choice(USER_AGENTS),   # from your pool
    "Accept": "text/html, */*; q=0.01",
    "Accept-Language": "en-US,en;q=0.9",
    "X-Requested-With": "XMLHttpRequest",
    "Referer": "https://dramabeans.com",        # often required
    "Connection": "keep-alive",
}
ALT_NAME_FOR_NAMES = [
    "Also known as",
    "Alt name",
    "Stage name",
    "Birth name",
]

class WikipediaKactorsSpider(scrapy.Spider):
    name = "wiki_kactors"
    allowed_domains = ["en.wikipedia.org"]
    start_urls = ["https://en.wikipedia.org/wiki/List_of_South_Korean_male_actors", "https://en.wikipedia.org/wiki/List_of_South_Korean_actresses"]

    # custom_settings = {
    #     "ITEM_PIPELINES": {
    #         "kdramavibe_scrapper.scrapper_spider.scrapper_spider.pipelines.WikipediaKactorsPipeline": 300,
    #     }
    # }

    def start_requests(self):
        for url in self.start_urls:
            if 'actresses' in url:
                gender = 'female'
            else:
                gender = 'male'

            headers = {
                "User-Agent": random.choice(USER_AGENTS),
                "Accept-Language": "en-US,en;q=0.9",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            }
            yield scrapy.Request(
                url=url,
                callback=self.parse,
                headers=headers,
                meta={"gender": gender}
            )


    def parse(self, response):
        # Get links to all drama pages
        for actor in response.css("div#mw-content-text div.div-col ul li a"):
            full_url = response.urljoin(actor.attrib['href'])
            item = KactorItem()
            item['gender'] = response.meta['gender']
            item['wikipedia_url'] = full_url

            yield scrapy.Request(url=full_url, callback=self.parse_kdrama,
                headers=AJAX_HEADERS, meta={"item": item})

        
    def parse_kdrama(self, response):
        item = response.meta['item']
        item['name'] = response.css("h1#firstHeading span.mw-page-title-main::text").get()
        infobox = response.css("table.infobox.biography")
        
        birthplace_div = infobox.css("th:contains('Born') + td div.birthplace")
        birthplace_text = (birthplace_div.xpath('string()').get() or '').strip()
        item['birthplace'] = birthplace_text if birthplace_text else None

        # --- Birthday & Age ---
        birthday_str = infobox.css("th:contains('Born') + td span.bday::text").get()
        if birthday_str:
            birthday_date = datetime.strptime(birthday_str, '%Y-%m-%d').date()
            today = datetime.today().date()
            age = today.year - birthday_date.year - ((today.month, today.day) < (birthday_date.month, birthday_date.day))
        else:
            birthday_date = None
            age = None

        item['birthday'] = birthday_date
        item['age'] = age

        item['description'] = self.get_description(infobox)
        print('\n******\n', infobox.css("th:contains('Years active') + td::text"), '\n******\n')
        years_active_texts = infobox.xpath(
            ".//tr[th[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'years active')]]//td//text()"
        ).getall()
        

        item['occupations'] = infobox.css("th:contains('Occupation') + td::text, th:contains('Occupation') +  td *:not(style)::text").getall()
        item['agent'] = infobox.css("th:contains('Agent') + td::text, th:contains('Agent') + td *:not(style)::text").get()
        
        item['height'] = infobox.css("th:contains('Height') + td::text, th:contains('Height') +  td *:not(style)::text").get()
        
        partner_texts = infobox.css(
            "th:contains('Spouse') + td::text, "
            "th:contains('Spouse') + td *:not(style)::text, "
            "th:contains('Partner') + td::text, "
            "th:contains('Partner') + td *:not(style)::text"
        ).getall()

        # Clean and join
        partner_texts = [p.strip() for p in partner_texts if p.strip()]
        item['partner_or_spouse'] = ", ".join(partner_texts) if partner_texts else None        
        item['image_url'] = f'https:{infobox.css("td.infobox-image a img.mw-file-element::attr(src)").get()}'

        
        yield item
    

    def get_description(self, infobox):
        biography_text = []
        
        if infobox:
            # Collect all following siblings until the next div with h2
            for sibling in infobox.xpath('following-sibling::*'):
                if sibling.xpath("self::div[contains(@class,'mw-heading')]"):
                    break
                if sibling.root.tag == 'p':
                    text = sibling.xpath('string()').get()
                    if text:
                        biography_text.append(text.strip())

        return " ".join(biography_text)