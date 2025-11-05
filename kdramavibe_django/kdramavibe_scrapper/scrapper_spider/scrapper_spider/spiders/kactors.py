import scrapy
import random
from datetime import datetime
from ..items import DramaBeansKactorItem

# -------------------------------
# User-Agent pool for randomizing requests
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
# Headers for AJAX requests
# -------------------------------
AJAX_HEADERS = {
    "User-Agent": random.choice(USER_AGENTS),   # Randomized User-Agent
    "Accept": "text/html, */*; q=0.01",
    "Accept-Language": "en-US,en;q=0.9",
    "X-Requested-With": "XMLHttpRequest",
    "Referer": "https://dramabeans.com",        # Often required by the site
    "Connection": "keep-alive",
}


class KactorsSpider(scrapy.Spider):
    """
    Spider to crawl K-actor profiles from Dramabeans.
    """
    name = "kactors"
    allowed_domains = ["dramabeans.com"]
    start_urls = ["https://dramabeans.com/celebs/"]

    # Custom settings for this spider
    custom_settings = {
        "ITEM_PIPELINES": {
            "kdramavibe_scrapper.scrapper_spider.scrapper_spider.pipelines.KactorPipeline": 300,
        }
    }

    def start_requests(self):
        """
        Start by sending a request to the main celebrity page
        with a randomized User-Agent.
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
        Parse the main list of K-actors on the site.
        Extract basic info and follow the link to the individual actor page.
        """
        for kactor in response.css("div.show-recap-detail"):
            kactoritem = DramaBeansKactorItem()
            kactoritem["image_url"] = kactor.css(
                "div.show-recap-detail-img img::attr(src)"
            ).get()

            kactoritem['name'] = kactor.css(
                "div.show-title-name a::text"
            ).get(default="").strip()

            kactoritem["dramabeans_url"] = kactor.css(
                "div.show-title-name a::attr(href)"
            ).get()

            kactoritem["no_of_votes"] = kactor.css(
                "div.show-number-review-rating span.number-rating::text"
            ).get()

            # Follow to the detailed actor page
            yield scrapy.Request(
                url=kactoritem['dramabeans_url'],
                callback=self.parse_kactor,
                headers=AJAX_HEADERS,
                meta={"item": kactoritem},
            )

        # -------------------------------
        # Pagination: Follow next page if exists
        # -------------------------------
        next_page = response.css("a.next.page-numbers::attr(href)").get()
        if next_page:
            yield response.follow(
                next_page,
                callback=self.parse,
                headers=AJAX_HEADERS
            )

    def parse_kactor(self, response):
        """
        Parse individual K-actor page to extract detailed info.
        """
        item = response.meta["item"]

        # Update the name in case it's more complete on this page
        item['name'] = response.css(
            "div.banner-title a h3::text"
        ).get().strip() or item['name']

        # Extract birthday
        birthdays = response.css("p.title-rate::text").getall()
        date_formats = ['%B %d, %Y', '%Y-%m-%d', '%d %B %Y']

        if birthdays:
            # Clean the string
            birthday_str = birthdays[0].replace("Birthdate: ", "").strip()
            
            birthday_date = None
            for fmt in date_formats:
                try:
                    birthday_date = datetime.strptime(birthday_str, fmt).date()
                    break  # Stop once we find a matching format
                except ValueError:
                    continue  # Try the next format
            
            item['birthday'] = birthday_date  # Will be a date object or None

        # Extract birthplace (first <p> in wrapper-user-rating)
        places = response.css("div.wrapper-user-rating p::text").getall()
        if places:
            item['birthplace'] = places[0].strip()

        # Yield the fully populated item
        yield item
