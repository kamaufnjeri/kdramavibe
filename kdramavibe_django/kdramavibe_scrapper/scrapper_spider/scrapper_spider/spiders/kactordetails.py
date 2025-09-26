import scrapy
from urllib.parse import quote
from ..items import KactorItem
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

class KactorDetailsSpider(scrapy.Spider):
    name = "kactor_details"
    allowed_domains = ["dramabeans.com"]

        
    custom_settings = {
        "ITEM_PIPELINES": {
            "kdramavibe_scrapper.scrapper_spider.scrapper_spider.pipelines.KactorDetailsPipeline": 300,
        }
    }
    def __init__(self, kactors=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # dramas is a list of tuples: (db_id, dramabeans_url)
        self.kactors = kactors or []

    def start_requests(self):
        for name, dramabeans_url in self.kactors:
            headers = {
                "User-Agent": random.choice(USER_AGENTS),
                "Accept-Language": "en-US,en;q=0.9",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            }
            yield scrapy.Request(
                url=dramabeans_url,
                callback=self.parse,
                meta={"name": name},
                headers=headers
            )

    def parse(self, response):
        item = KactorItem()

        bio_div = response.css("div#bind_tab_bio")
        description_div = response.css("div.banner-description")

        item['name'] = response.css("div.banner-title a h3::text").get(default="").strip()
        item['description'] = description_div.xpath("string()").get(default="").strip()
        item['bio'] = bio_div.xpath("string()").get(default="").strip()
        
        item['kdramas'] = response.xpath(
            '//div[@class="banner-type"]//span//a[@class="post_tags"]/text()'
        ).getall()
        item['dramabeans_url'] = response.url

        birthdays = response.css("p.title-rate::text").getall()
        if birthdays:
            item['birthday'] = birthdays[0].replace("birthday:", "").strip()

        # ✅ Birthplace (first wrapper-user-rating p)
        places = response.css("div.wrapper-user-rating p::text").getall()
        if places:
            item['birthplace'] = places[0].strip()


        yield item




# import scrapy
# from urllib.parse import quote
# from ..items import KactorItem


# class KactorDetailsSpider(scrapy.Spider):
#     name = "kactor_details"
#     allowed_domains = ["dramabeans.com"]

#     def __init__(self, dramabeans_url=None, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         if not dramabeans_url:
#             raise ValueError("Dramabeans url is needed")
#         self.start_urls = [dramabeans_url]
        
#     custom_settings = {
#         "ITEM_PIPELINES": {
#             "kdramavibe_scrapper.scrapper_spider.scrapper_spider.pipelines.KactorDetailsPipeline": 300,
#         }
#     }

#     def parse(self, response):
#         item = KactorItem()

#         bio_div = response.css("div#bind_tab_bio")
#         description_div = response.css("div.banner-description")

#         item['name'] = response.css("div.banner-title a h3::text").get(default="").strip()
#         item['description'] = description_div.xpath("string()").get(default="").strip()
#         item['bio'] = bio_div.xpath("string()").get(default="").strip()
        
#         item['kdramas'] = response.xpath(
#             '//div[@class="banner-type"]//span//a[@class="post_tags"]/text()'
#         ).getall()
#         item['dramabeans_url'] = response.url

#         birthdays = response.css("p.title-rate::text").getall()
#         if birthdays:
#             item['birthday'] = birthdays[0].replace("birthday:", "").strip()

#         # ✅ Birthplace (first wrapper-user-rating p)
#         places = response.css("div.wrapper-user-rating p::text").getall()
#         if places:
#             item['birthplace'] = places[0].strip()


#         yield item
