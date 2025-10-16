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
    "Characters",
    "Main Cast",
    "Supporting Cast",
    "Recurring Cast",
    "Guest Cast",
    "Special Appearances",
    "Main Characters",
    "Recurring Characters",
    "Guest Characters"
]

class SingleKdramaSpider(scrapy.Spider):
    name = "single_kdrama"
    allowed_domains = ["en.wikipedia.org"]
   
    custom_settings = {
        "ITEM_PIPELINES": {
            "kdramavibe_scrapper.scrapper_spider.scrapper_spider.pipelines.WikipediaKdramaPipeline": 300,
        }
    }

    def __init__(self, start_url=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if start_url is None:
            raise ValueError("You must provide start_url!")
        self.start_urls = [start_url]

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
        url = response.url
        item = KdramaItem()
        item['wikipedia_url'] = url        
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
        ref_pattern = re.compile(r'\[(\d+|[a-z]+)\]', re.IGNORECASE)

        casts = []

        for name in ALT_NAMES_FOR_CASTS:
            # Locate the div with the target section heading
            div_selector = response.xpath(
                f"//div[contains(@class,'mw-heading') and contains(@class,'mw-heading2')]/h2[normalize-space(text())='{name}']/parent::div"
            )

            if not div_selector:
                continue

            # Loop through siblings until the next section
            for sibling in div_selector.xpath('following-sibling::*'):

                # Stop at next heading
                if sibling.xpath("self::div[contains(@class,'mw-heading2')]"):
                    break

                # ---------- Handle bullet lists ----------
                if sibling.root.tag == 'ul':
                    for li in sibling.xpath('.//li'):
                        # Get the text of the <li> **excluding <sup> nodes**
                        full_text = ''.join(li.xpath('.//text()[not(ancestor::sup)]').getall()).strip()

                        # Get actor name and URL from first <a> not inside a <sup>
                        actor_name = li.xpath('.//a[not(ancestor::sup)][1]/text()').get()
                        actor_url = li.xpath('.//a[not(ancestor::sup)][1]/@href').get()

                        role_name = None
                        if actor_name and actor_name in full_text:
                            role_text = full_text.replace(actor_name, '').strip()
                            role_text = re.sub(r'^\s*(as|–|-)\s*', '', role_text, flags=re.I)
                            role_text = re.sub(r'\[.*?\]', '', role_text).strip()  # remove bracketed refs
                            role_name = role_text if role_text else None

                        if actor_name and actor_url:
                            casts.append({
                                'actor_name': actor_name.strip(),
                                'role_name': role_name,
                                'actor_url': response.urljoin(actor_url)
                            })

                if sibling.root.tag == 'table':
                    rows = sibling.xpath('.//tr')
                    if not rows:
                        return casts  # skip empty tables

                    # Get header row
                    headers = [th.xpath('string()').get().strip().lower() for th in rows[0].xpath('.//th')]
                    actor_idx = next((i for i, h in enumerate(headers) if 'actor' in h or 'cast' in h), None)
                    role_idx = next((i for i, h in enumerate(headers) if 'character' in h or 'role' in h), None)

                    for tr in rows[1:]:
                        tds = tr.xpath('.//td')
                        if not tds:
                            continue

                        actor_name = None
                        actor_url = None

                        if actor_idx is not None:
                            # Only consider <a> tags, ignore <sup>
                            a_tag = tds[actor_idx].xpath('.//a[not(ancestor::sup)]')
                            if a_tag:
                                actor_name = a_tag.xpath('string()').get().strip()
                                actor_url = a_tag.xpath('@href').get()
                                if actor_url:
                                    actor_url = response.urljoin(actor_url)

                        role_name = None
                        if role_idx is not None:
                            role_name = tds[role_idx].xpath('string()').get()
                            if role_name:
                                role_name = ref_pattern.sub('', role_name).strip()

                        if actor_name and actor_url:
                            casts.append({
                                'actor_name': actor_name,
                                'role_name': role_name if role_name else None,
                                'actor_url': actor_url
                            })
                            # Stop after first matching section
            break

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
                    if sibling.xpath("self::div[contains(@class,'mw-heading2')]"):
                        break
                    if sibling.root.tag == 'p':
                        text = sibling.xpath('string()').get()
                        if text:
                            plot_text.append(text.strip())
                break  # stop after the first matching section

        return " ".join(plot_text)