import scrapy
import random
from urllib.parse import quote
from ..items import KdramaItem

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
    "Referer": "https://dramabeans.com",        # Often required
    "Connection": "keep-alive",
}


class KdramasSpider(scrapy.Spider):
    """
    Spider to crawl K-drama recaps from Dramabeans.
    """
    name = "kdramas"
    allowed_domains = ["dramabeans.com"]
    start_urls = ["https://dramabeans.com/recaps/all/"]

    # Custom pipeline settings for this spider
    custom_settings = {
        "ITEM_PIPELINES": {
            "kdramavibe_scrapper.scrapper_spider.scrapper_spider.pipelines.KdramaPipeline": 300,
        }
    }

    def start_requests(self):
        """
        Start by sending a request to the main recap page with a randomized User-Agent.
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
        Parse the main list of K-dramas.
        Extract basic info such as title, URL, rating, and number of votes.
        """
        for kdrama in response.css("div.show-recap-detail"):
            kdramaitem = KdramaItem()

            kdramaitem["title"] = kdrama.css(
                "div.show-title-name a::text"
            ).get(default="").strip()

            kdramaitem["dramabeans_url"] = kdrama.css(
                "div.show-title-name a::attr(href)"
            ).get()

            kdramaitem["rating"] = kdrama.css(
                "div.show-rating span.review-rating::text"
            ).get()

            kdramaitem["no_of_votes"] = kdrama.css(
                "div.show-number-review-rating span.number-rating::text"
            ).get()

            yield kdramaitem

        # -------------------------------
        # Pagination: Follow next page if available
        # -------------------------------
        next_page = response.css("a.next.page-numbers::attr(href)").get()
        if next_page:
            yield response.follow(
                next_page,
                callback=self.parse,
                headers=AJAX_HEADERS
            )

    # -------------------------------
    # Detailed parsing for individual dramas (currently commented out)
    # -------------------------------
    # def parse_kdrama(self, response):
    #     """
    #     Extract detailed info such as description, genres, and cast.
    #     """
    #     item = response.meta["item"]
    #     description_div = response.css("div.banner-description")
    #
    #     item['rating']  = response.css('div.banner-title-rate span.rating::text').get() or item['rating']
    #     item['total_rating']  = response.css('div.banner-title-rate span.total-rating::text').get()
    #     item['description'] = description_div.xpath("string()").get(default="").strip()
    #     item['genres'] = response.xpath(
    #         '//div[@class="banner-type"]//span//a[@class="post_tags"]/text()'
    #     ).getall()
    #
    #     show_id = response.css("input#show_id::attr(value)").get()
    #     title = item['title'] or "Unknown"
    #
    #     ajax_url = (
    #         "https://dramabeans.com/casts/"
    #         f"?show_id={show_id}&tag={quote(title)}&order=desc&shows=shows&select_ajax=select_ajax"
    #     )
    #
    #     yield scrapy.Request(
    #         url=ajax_url,
    #         callback=self.parse_casts,
    #         headers=AJAX_HEADERS,
    #         meta={"item": item},
    #     )
    #
    # def parse_casts(self, response):
    #     """
    #     Parse the AJAX response to extract cast details for each drama.
    #     """
    #     item = response.meta["item"]
    #     kactors_list = []
    #
    #     for cast in response.css("#show_casts .casts-detail"):
    #         name = cast.css(".casts-name a::text").get()
    #         role = cast.css(".casts-character-name::text").get()
    #         dramabeans_url = cast.css(".casts-name a::attr(href)").get()
    #
    #         if name and role:
    #             kactors_list.append({
    #                 "name": name.strip(),
    #                 "role": role.strip(),
    #                 "dramabeans_url": dramabeans_url,
    #             })
    #
    #     item["kactors"] = kactors_list
    #     yield item
