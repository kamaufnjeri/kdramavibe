import scrapy
from ..items import KdramaItem  # your Scrapy item
import random
import re

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_3) AppleWebKit/605.1.15 "
    "(KHTML, like Gecko) Version/17.0 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 "
    "(KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 17_2 like Mac OS X) AppleWebKit/605.1.15 "
    "(KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_2_1) AppleWebKit/605.1.15 "
    "(KHTML, like Gecko) Version/17.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) Gecko/20100101 Firefox/124.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
]

AJAX_HEADERS = {
    "User-Agent": random.choice(USER_AGENTS),  # choose randomly from the pool
    "Accept": "text/html, */*; q=0.01",
    "Accept-Language": "en-US,en;q=0.9",
    "X-Requested-With": "XMLHttpRequest",
    "Referer": "https://dramabeans.com",  # sometimes required
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


class WikipediaKdramasSpider(scrapy.Spider):
    """
    Spider to scrape Korean dramas from Wikipedia, including
    title, plot, cast, directors, writers, episodes, and other info.
    """
    name = "wiki_kdramas"
    allowed_domains = ["en.wikipedia.org"]
    start_urls = ["https://en.wikipedia.org/wiki/List_of_Korean_dramas"]

    custom_settings = {
        "ITEM_PIPELINES": {
            "kdramavibe_scrapper.scrapper_spider.scrapper_spider.pipelines.WikipediaKdramaPipeline": 300,
        }
    }

    def start_requests(self):
        """
        Initial request to the drama list page with random User-Agent.
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
        Parse the list of dramas and extract links to each drama's page.
        """
        for drama in response.css("div#mw-content-text ul li i a"):
            full_url = response.urljoin(drama.attrib["href"])
            item = KdramaItem()
            item["wikipedia_url"] = full_url

            # Request the individual drama page
            yield scrapy.Request(
                url=full_url,
                callback=self.parse_kdrama,
                headers=AJAX_HEADERS,
                meta={"item": item}
            )

    def parse_kdrama(self, response):
        """
        Parse an individual drama page for detailed information:
        title, genres, episodes, networks, directors, writers,
        running time, seasons, country, languages, image, cast,
        alternate titles, plot, and start/end years.
        """
        item = response.meta["item"]
        item["title"] = response.css("h1#firstHeading i::text").get()
        infobox = response.css("table.infobox.ib-tv")

        # Extract standard infobox info
        item["genres"] = infobox.css(
            "th:contains('Genre') + td::text, th:contains('Genre') + td *:not(style)::text"
        ).getall()
        item["episodes"] = infobox.css(
            "th:contains('No. of episodes') + td::text, th:contains('No. of episodes') + td *:not(style)::text"
        ).get()
        item["networks"] = infobox.css(
            "th:contains('Network') + td::text, th:contains('Network') + td *:not(style)::text"
        ).getall()
        release_dates = infobox.css(
            "th:contains('Release') + td::text, th:contains('Release') + td *:not(style):not(span)::text"
        ).getall()
        item["directors"] = infobox.css(
            "th:contains('Directed by') + td::text, th:contains('Directed by') + td *:not(style)::text"
        ).getall()
        item["writers"] = infobox.css(
            "th:contains('Written by') + td::text, th:contains('Written by') + td *:not(style)::text, "
            "th:contains('Screenplay by') + td::text, th:contains('Screenplay by') + td *:not(style)::text"
        ).getall()
        item["running_time"] = infobox.css(
            "th:contains('Running time') + td::text"
        ).get()
        item["seasons"] = infobox.css(
            "th:contains('No. of seasons') + td::text"
        ).get()
        item["country"] = infobox.css(
            "th:contains('Country of origin') + td::text"
        ).get()
        item["languages"] = infobox.css(
            "th:contains('Original language') + td::text, th:contains('Original language') + td *:not(style)::text"
        ).getall()
        item["image_url"] = f'https:{infobox.css("td.infobox-image a img.mw-file-element::attr(src)").get()}'

        # Extract cast and other structured fields
        item["kactors"] = self.get_casts(response)

        # Alternate titles
        alt_name_selectors = ", ".join([
            f"th:contains('{field}') + td::text, th:contains('{field}') + td *:not(style):not(span)::text"
            for field in ALT_NAME_FOR_TITLE
        ])
        item["alternate_titles"] = infobox.css(alt_name_selectors).getall()

        # Plot section
        item["plot"] = self.get_plot(response)

        # Start and end years
        start_year, end_year = self.get_start_and_end_years(release_dates)
        item["start_year"] = start_year
        item["end_year"] = end_year

        yield item

    def get_start_and_end_years(self, release_dates):
        """
        Extract the start and end year from release date text.
        Returns a tuple (start_year, end_year), with 'PRESENT' for ongoing dramas.
        """
        years = []
        start_year = None
        end_year = None
        for date in release_dates:
            if "present" in date.lower():
                end_year = "PRESENT"
            found = re.findall(r"\b(?:19|20)\d{2}\b", date)
            years.extend(found)

        if years:
            start_year = min(years)
            if end_year != "PRESENT":
                end_year = max(years)
        return start_year, end_year

    def get_casts(self, response):
        """
        Extract cast information from the drama page, including actor name,
        role name, and actor Wikipedia URL. Handles bullet lists and tables.
        """
        ref_pattern = re.compile(r"\[(\d+|[a-z]+)\]", re.IGNORECASE)
        casts = []

        for name in ALT_NAMES_FOR_CASTS:
            div_selector = response.xpath(
                f"//div[contains(@class,'mw-heading') and contains(@class,'mw-heading2')]/h2"
                f"[normalize-space(text())='{name}']/parent::div"
            )
            if not div_selector:
                continue

            # Iterate siblings until next section
            for sibling in div_selector.xpath("following-sibling::*"):
                if sibling.xpath("self::div[contains(@class,'mw-heading2')]"):
                    break

                # Bullet lists
                if sibling.root.tag == "ul":
                    for li in sibling.xpath(".//li"):
                        full_text = "".join(li.xpath(".//text()[not(ancestor::sup)]").getall()).strip()
                        actor_name = li.xpath(".//a[not(ancestor::sup)][1]/text()").get()
                        actor_url = li.xpath(".//a[not(ancestor::sup)][1]/@href").get()
                        role_name = None
                        if actor_name and actor_name in full_text:
                            role_text = full_text.replace(actor_name, "").strip()
                            role_text = re.sub(r"^\s*(as|–|-)\s*", "", role_text, flags=re.I)
                            role_text = re.sub(r"\[.*?\]", "", role_text).strip()
                            role_name = role_text if role_text else None
                        if actor_name and actor_url:
                            casts.append({
                                "actor_name": actor_name.strip(),
                                "role_name": role_name,
                                "actor_url": response.urljoin(actor_url)
                            })

                # Tables
                if sibling.root.tag == "table":
                    rows = sibling.xpath(".//tr")
                    if not rows:
                        return casts
                    headers = [th.xpath("string()").get().strip().lower() for th in rows[0].xpath(".//th")]
                    actor_idx = next((i for i, h in enumerate(headers) if "actor" in h or "cast" in h), None)
                    role_idx = next((i for i, h in enumerate(headers) if "character" in h or "role" in h), None)

                    for tr in rows[1:]:
                        tds = tr.xpath(".//td")
                        if not tds:
                            continue

                        actor_name = None
                        actor_url = None
                        if actor_idx is not None:
                            a_tag = tds[actor_idx].xpath(".//a[not(ancestor::sup)]")
                            if a_tag:
                                actor_name = a_tag.xpath("string()").get().strip()
                                actor_url = a_tag.xpath("@href").get()
                                if actor_url:
                                    actor_url = response.urljoin(actor_url)

                        role_name = None
                        if role_idx is not None:
                            role_name = tds[role_idx].xpath("string()").get()
                            if role_name:
                                role_name = ref_pattern.sub("", role_name).strip()

                        if actor_name and actor_url:
                            casts.append({
                                "actor_name": actor_name,
                                "role_name": role_name if role_name else None,
                                "actor_url": actor_url
                            })
            break  # Stop after first matching section

        return casts

    def get_plot(self, response):
        """
        Extract plot/synopsis from drama page. Combines all paragraphs
        under the first matching plot section.
        """
        plot_text = []
        for name in ALT_NAMES_FOR_PLOT:
            div_selector = response.xpath(
                f"//div[contains(@class,'mw-heading') and contains(@class,'mw-heading2')]/h2"
                f"[normalize-space(text())='{name}']/parent::div"
            )
            if div_selector:
                for sibling in div_selector.xpath("following-sibling::*"):
                    if sibling.xpath("self::div[contains(@class,'mw-heading2')]"):
                        break
                    if sibling.root.tag == "p":
                        text = sibling.xpath("string()").get()
                        if text:
                            plot_text.append(text.strip())
                break
        return " ".join(plot_text)
