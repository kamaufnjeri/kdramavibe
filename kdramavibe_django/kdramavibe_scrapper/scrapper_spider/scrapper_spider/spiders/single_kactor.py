import scrapy
import random
import re
from datetime import datetime
from ..items import KactorItem
from ..clean_data import cleaner

# -------------------------------
# User-Agent pool for requests
# -------------------------------
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

# -------------------------------
# AJAX headers for requests
# -------------------------------
AJAX_HEADERS = {
    "User-Agent": random.choice(USER_AGENTS),
    "Accept": "text/html, */*; q=0.01",
    "Accept-Language": "en-US,en;q=0.9",
    "X-Requested-With": "XMLHttpRequest",
    "Referer": "https://dramabeans.com",
    "Connection": "keep-alive",
}

# Fields in Wikipedia infobox that may contain alternate names
ALT_NAME_FOR_NAMES = [
    "Also known as",
    "Alt name",
    "Stage name",
    "Birth name",
]


class SingleKactorSpider(scrapy.Spider):
    """
    Spider to scrape a single K-actor's Wikipedia page.
    """
    name = "single_kactor"
    allowed_domains = ["en.wikipedia.org"]

    custom_settings = {
        "ITEM_PIPELINES": {
            "kdramavibe_scrapper.scrapper_spider.scrapper_spider.pipelines.WikipediaKactorPipeline": 300,
        }
    }

    def __init__(self, start_url=None, *args, **kwargs):
        """
        Require a start_url for the actor's Wikipedia page.
        """
        super().__init__(*args, **kwargs)
        if start_url is None:
            raise ValueError("You must provide start_url!")
        self.start_urls = [start_url]

    def start_requests(self):
        """
        Send initial request with randomized User-Agent.
        """
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
        """
        Parse the actor's Wikipedia page to extract information from infobox and main content.
        """
        item = KactorItem()
        item['wikipedia_url'] = response.url
        item['name'] = response.css("h1#firstHeading span.mw-page-title-main::text").get()
        item['description'] = self.get_description(response)

        # Select possible infoboxes
        infobox_sel = response.css(
            "table.infobox.biography, table.infobox.vcard, table.infobox.plainlist"
        )
        infobox = infobox_sel[0] if infobox_sel else None

        if infobox:
            # --- Alternate names ---
            alt_name_selectors = ", ".join([
                f"th:contains('{field}') + td::text, th:contains('{field}') + td *:not(style):not(span)::text"
                for field in ALT_NAME_FOR_NAMES
            ])
            birthname_div = infobox.css("th:contains('Born') + td div.nickname")
            birthname_text = (birthname_div.xpath('string()').get() or '').strip()

            alt_names = infobox.css(alt_name_selectors).getall()
            if birthname_text:
                alt_names.append(birthname_text)
            item['alternate_names'] = alt_names

            # --- Birthplace ---
            birthplace_div = infobox.css("th:contains('Born') + td div.birthplace")
            birthplace_text = (birthplace_div.xpath('string()').get() or '').strip()
            if not birthplace_text:
                birthplace_td = infobox.css("th:contains('Origin') + td")
                birthplace_text = (birthplace_td.xpath('string()').get() or '').strip()
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

            # --- Years active ---
            years_active = infobox.xpath(
                'string(.//tr[th[contains(normalize-space(translate(., "\u00A0", " ")), "Years active")]]/td)'
            ).get()
            item['years_active'] = years_active.strip() if years_active else None

            # --- Occupation, agents, height ---
            item['occupations'] = infobox.css(
                "th:contains('Occupation') + td::text, th:contains('Occupation') + td *:not(style)::text"
            ).getall()
            item['agents'] = infobox.css(
                "th:contains('Agent') + td::text, th:contains('Agent') + td *:not(style)::text"
            ).getall()
            item['height'] = infobox.css(
                "th:contains('Height') + td::text, th:contains('Height') + td *:not(style)::text"
            ).get()

            # --- Partner/Spouse & Children ---
            item['partner_or_spouse'] = self.get_partner_or_spouse(infobox)
            item['children'] = self.get_children(infobox)

            # --- Image URL ---
            item['image_url'] = f'https:{infobox.css("td.infobox-image a img.mw-file-element::attr(src)").get()}'

        yield item

    # -------------------------------
    # Helper functions
    # -------------------------------
    def get_description(self, response):
        """
        Extract the actor's biography description from page content.
        """
        biography_text = []
        infobox_sel = response.css(
            "table.infobox.biography, table.infobox.vcard, table.infobox.plainlist"
        )
        infobox = infobox_sel[0] if infobox_sel else None
        elements = infobox.xpath('following-sibling::*') if infobox else response.xpath('//div[@id="mw-content-text"]/*')

        for sibling in elements:
            if sibling.xpath('self::div[contains(@class,"mw-heading2")] | self::h2'):
                break
            if sibling.root.tag == 'p':
                text = sibling.xpath('string()').get()
                if text and text.strip():
                    biography_text.append(text.strip())
            elif sibling.root.tag in ['ul', 'ol']:
                for li in sibling.xpath('.//li'):
                    li_text = li.xpath('string()').get()
                    if li_text and li_text.strip():
                        biography_text.append(li_text.strip())

        full_text = " ".join(biography_text)
        full_text = re.sub(r'\[\d+\]', '', full_text)
        return full_text.strip() if full_text else None

    def get_partner_or_spouse(self, infobox):
        """
        Extract and clean partner or spouse information from infobox.
        """
        partner_texts = infobox.css(
            "th:contains('Spouse') + td::text, "
            "th:contains('Spouse') + td *:not(style)::text, "
            "th:contains('Partner') + td::text, "
            "th:contains('Partner') + td *:not(style)::text"
        ).getall()

        cleaned = []
        for p in partner_texts:
            text = p.strip()
            if not text:
                continue
            text = re.sub(r"[\u200b\u200c\u200d\uFEFF]", "", text)
            text = re.sub(r"\s*,\s*(?=[);])", "", text)
            text = re.sub(r",\s*,+", ", ", text)
            text = re.sub(r"\s{2,}", " ", text)
            cleaned.append(text)

        partner_str = " ".join(cleaned)
        partner_str = re.sub(r"\s*([,;])\s*", r"\1 ", partner_str)
        partner_str = partner_str.strip(" ,;")
        return partner_str if partner_str else None

    def get_children(self, infobox):
        """
        Extract and clean children information from infobox.
        """
        children_raw = infobox.xpath('string(.//tr[th[contains(text(), "Children")]]/td)').get()
        children_raw = children_raw.strip() if children_raw else ""

        if children_raw:
            children_raw = re.sub(r"[\u200b\u200c\u200d\uFEFF]", "", children_raw)
            children_raw = re.sub(r"\s+", " ", children_raw)

            children_list = []
            num_match = re.search(r'\b(\d+)\b', children_raw)
            if num_match:
                children_list.append(int(num_match.group(1)))

            name_matches = re.findall(r"\b[A-Z][a-z]+(?:\s[A-Z][a-z]+)*\b", children_raw)
            blacklist = {"Child", "Children", "Including"}
            names = [n for n in name_matches if n not in blacklist]

            if names:
                children_list.extend(names)

            return children_list if children_list else [children_raw]
        else:
            return []
