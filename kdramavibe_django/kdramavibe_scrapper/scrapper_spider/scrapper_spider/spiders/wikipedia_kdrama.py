import scrapy
from ..items import KdramaItem  # your Scrapy item
import random
import re


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

ALT_NAME_FOR_TITLE = [
    "Also known as",
    "Alt name",
    "Original title",
    "Direct translation",
    "Lit."
]

ALT_NAMES_FOR_PLOT = [
    "Plot",
    "Synopsis",
    "Premise",
    "Story",
    "Summary",
    "Plot summary",
    "Background",
    "Overview"
]
ALT_NAMES_FOR_CASTS = [
    "Cast",
    "Cast and characters",
    "Characters"
]

class WikipediaKdramasSpider(scrapy.Spider):
    name = "wiki_kdramas"
    allowed_domains = ["en.wikipedia.org"]
    start_urls = ["https://en.wikipedia.org/wiki/List_of_Korean_dramas"]

    custom_settings = {
        "ITEM_PIPELINES": {
            "kdramavibe_scrapper.scrapper_spider.scrapper_spider.pipelines.WikipediaKdramaPipeline": 300,
        }
    }

    def start_requests(self):
        headers = {
            "User-Agent": random.choice(USER_AGENTS),
            "Accept-Language": "en-US,en;q=0.9",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        }
        yield scrapy.Request(
            url=self.start_urls[0],
            callback=self.parse,
            headers=headers
        )


    def parse(self, response):
        # Get links to all drama pages
        for drama in response.css("div#mw-content-text ul li i a"):
            full_url = response.urljoin(drama.attrib['href'])
            item = KdramaItem()
            item['wikipedia_url'] = full_url

            yield scrapy.Request(url=full_url, callback=self.parse_kdrama,
                headers=AJAX_HEADERS, meta={"item": item})

        
    def parse_kdrama(self, response):
        item = response.meta['item']
        item['title'] = response.css("h1#firstHeading i::text").get()
        infobox = response.css("table.infobox.ib-tv")
        item['genres'] = infobox.css("th:contains('Genre') + td::text, th:contains('Genre') + td *:not(style)::text").getall()
        item['episodes'] = infobox.css("th:contains('No. of episodes') + td::text, th:contains('No. of episodes') +  td *:not(style)::text").get()
        item['networks'] = infobox.css("th:contains('Network') + td::text, th:contains('Network') + td *:not(style)::text").getall()
        release_dates = infobox.css("th:contains('Release') + td::text, th:contains('Release') + td *:not(style):not(span)::text").getall()
        item['directors'] = infobox.css("th:contains('Directed by') + td::text, th:contains('Directed by') +  td *:not(style)::text").getall()
        item['writers'] = infobox.css("th:contains('Written by') + td::text, th:contains('Written by') + td *:not(style)::text, th:contains('Screenplay by') + td::text, th:contains('Screenplay by') + td *:not(style)::text").getall()
        item['running_time'] = infobox.css("th:contains('Running time') + td::text").get()
        item['seasons'] = infobox.css("th:contains('No. of seasons') + td::text").get()
        item['country'] = infobox.css("th:contains('Country of origin') + td::text").get()
        item['languages'] = infobox.css("th:contains('Original language') + td::text, th:contains('Original language') + td *:not(style)::text").getall()
        item['image_url'] = f'https:{infobox.css("td.infobox-image a img.mw-file-element::attr(src)").get()}'
        item['kactors'] = self.get_casts(response)
        alt_name_selectors = ", ".join([
            f"th:contains('{field}') + td::text, th:contains('{field}') + td *:not(style):not(span)::text"
            for field in ALT_NAME_FOR_TITLE
        ])
        item['alternate_titles'] =  infobox.css(alt_name_selectors).getall()
        item['plot'] = self.get_plot(response)
        start_year, end_year = self.get_start_and_end_years(release_dates)
        item['start_year'] = start_year
        item['end_year'] = end_year
        
        yield item
    
    def get_start_and_end_years(self, release_dates):
        years = []
        start_year = None
        end_year = None
        for date in release_dates:
            if "present" in date.lower():
                end_year = "PRESENT"
            found = re.findall(r'\b(?:19|20)\d{2}\b', date)
            
            for y in found:
                years.append(y)
        if years:
            start_year = min(years)
            if end_year != "PRESENT":
                end_year = max(years)
        return start_year, end_year
 
    def get_casts(self, response):
        casts = []

        for name in ALT_NAMES_FOR_CASTS:
            # Find the div with the target cast heading
            div_selector = response.xpath(
                f"//div[contains(@class,'mw-heading') and contains(@class,'mw-heading2')]/h2[normalize-space(text())='{name}']/parent::div"
            )

            if div_selector:
                # Loop through following siblings until next heading
                for sibling in div_selector.xpath('following-sibling::*'):

                    if sibling.xpath("self::div[contains(@class,'mw-heading2')]"):
                        break  # stop when next section starts

                    if sibling.root.tag == 'ul':
                        for li in sibling.xpath('.//li'):
                            actor_name = li.xpath('.//a[text() = @title]/text()').get()
                            actor_url = li.xpath('.//a[text() = @title]/@href').get()
                            full_text = li.xpath('string()').get()

                            role = None
                            if ' as ' in full_text:
                                full_text_split = full_text.split(' as ', 1)
                                if not actor_name and full_text_split[0] is not "":
                                    actor_name = full_text_split[0].strip()
                                role = full_text_split[1].strip()

                            if actor_name:
                                casts.append({
                                    'actor': actor_name.strip(),
                                    'url': response.urljoin(actor_url) if actor_url else None,
                                    'role': role
                                })
                break  # stop after first matching section

        return casts

    def get_plot(self, response):
        plot_text = []
        for name in ALT_NAMES_FOR_PLOT:
            div_selector = response.xpath(
                f"//div[contains(@class,'mw-heading') and contains(@class,'mw-heading2')]/h2[normalize-space(text())='{name}']/parent::div"
            )  
            if div_selector:
                # Collect all following siblings until the next div with h2
                for sibling in div_selector.xpath('following-sibling::*'):
                    if sibling.xpath("self::div[contains(@class,'mw-heading')]"):
                        break
                    if sibling.root.tag == 'p':
                        text = sibling.xpath('string()').get()
                        if text:
                            plot_text.append(text.strip())
                break  # stop after the first matching section

        return " ".join(plot_text)