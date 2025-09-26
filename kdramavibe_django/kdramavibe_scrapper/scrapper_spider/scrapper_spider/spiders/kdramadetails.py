import scrapy
from urllib.parse import quote
from django.conf import settings



from kdramavibe_scrapper.models import Kdrama
from ..items import KdramaItem

# kdramadetails.py (at the top)
import random

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
class KdramaDetailsSpider(scrapy.Spider):
    name = "kdrama_details"
    allowed_domains = ["dramabeans.com"]

    custom_settings = {
        "ITEM_PIPELINES": {
            "kdramavibe_scrapper.scrapper_spider.scrapper_spider.pipelines.KdramaDetailsPipeline": 300,
        }
    }

    def __init__(self, kdramas=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # dramas is a list of tuples: (db_id, dramabeans_url)
        self.kdramas = kdramas or []

    def start_requests(self):
        for title, dramabeans_url in self.kdramas:
            headers = {
                "User-Agent": random.choice(USER_AGENTS),
                "Accept-Language": "en-US,en;q=0.9",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            }
            yield scrapy.Request(
                url=dramabeans_url,
                callback=self.parse,
                meta={"title": title},
                headers=headers
            )

    def parse(self, response):
        item = KdramaItem()
        description_div = response.css("div.banner-description")

        item['title'] = response.css('div.banner-title a h3::text').get()
        item['rating']  = response.css('div.banner-title-rate span.rating::text').get()
        item['total_rating']  = response.css('div.banner-title-rate span.total-rating::text').get()
        item['description'] = description_div.xpath("string()").get(default="").strip()
        item['genre'] = response.xpath(
            '//div[@class="banner-type"]//span//a[@class="post_tags"]/text()'
        ).getall()
        item['dramabeans_url'] = response.url

        show_id = response.css("input#show_id::attr(value)").get()
        title = item['title'] or "Unknown"

        ajax_url = (
            "https://dramabeans.com/casts/"
            f"?show_id={show_id}&tag={quote(title)}&order=desc&shows=shows&select_ajax=select_ajax"
        )

        yield scrapy.Request(
            url=ajax_url,
            callback=self.parse_casts,
            headers=AJAX_HEADERS,
            meta={"item": item},
        )

    def parse_casts(self, response):
        item = response.meta["item"]
        kactors_list = []

        for cast in response.css("#show_casts .casts-detail"):
            name = cast.css(".casts-name a::text").get()
            role = cast.css(".casts-character-name::text").get()
            dramabeans_url = cast.css(".casts-name a::attr(href)").get()

            if name and role:
                kactors_list.append({
                    "name": name.strip(),
                    "role": role.strip(),
                    "dramabeans_url": dramabeans_url,
                })

        item["kactors"] = kactors_list
        yield item


# import scrapy
# from urllib.parse import quote
# from ..items import KdramaItem


# class KdramaDetailsSpider(scrapy.Spider):
#     name = "kdrama_details"
#     allowed_domains = ["dramabeans.com"]


#     def __init__(self, dramabeans_url=None, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         if not dramabeans_url:
#             raise ValueError("Dramabeans url is needed")
#         self.start_urls = [dramabeans_url]

#     custom_settings = {
#         "ITEM_PIPELINES": {
#             "kdramavibe_scrapper.scrapper_spider.scrapper_spider.pipelines.KdramaDetailsPipeline": 300,
#         }
#     }

#     def parse(self, response):
#         """Parse main show page details and schedule AJAX call for casts."""
#         item = KdramaItem()
#         description_div = response.css("div.banner-description")

#         item['title'] = response.css('div.banner-title a h3::text').get()
#         item['rating']  = response.css('div.banner-title-rate span.rating::text').get()
#         item['total_rating']  = response.css('div.banner-title-rate span.total-rating::text').get()
#         item['description'] = description_div.xpath("string()").get(default="").strip()
#         item['genre'] = response.xpath(
#             '//div[@class="banner-type"]//span//a[@class="post_tags"]/text()'
#         ).getall()
#         item['dramabeans_url'] = response.url

#         # Extract show_id from page (in HTML attrs or URL)
#         show_id = response.css("input#show_id::attr(value)").get()


#         # Build AJAX URL for casts
#         title = item['title'] or "Unknown"
#         ajax_url = (
#             "https://dramabeans.com/casts/"
#             f"?show_id={show_id}&tag={quote(title)}&order=desc&shows=shows&select_ajax=select_ajax"
#         )

#         # Pass item forward to next parser
#         yield scrapy.Request(
#             url=ajax_url,
#             callback=self.parse_casts,
#             meta={"item": item},
#         )

#     def parse_casts(self, response):
#         """Parse the AJAX-loaded cast list and attach to item."""
#         item = response.meta["item"]

#         kactors_list = []
#         for cast in response.css("#show_casts .casts-detail"):
#             name = cast.css(".casts-name a::text").get()
#             role = cast.css(".casts-character-name::text").get()
#             dramabeans_url = cast.css(".casts-name a::attr(href)").get()

#             if name and role:
#                 kactors_list.append({
#                     "name": name.strip(),
#                     "role": role.strip(),
#                     "dramabeans_url": dramabeans_url,
#                 })

#         item["kactors"] = kactors_list
#         yield item
