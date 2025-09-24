import scrapy
from ..items import KdramaItem

class KdramasSpider(scrapy.Spider):
    name = "kdramas"
    allowed_domains = ["dramabeans.com"]
    start_urls = ["https://dramabeans.com/recaps/all/"]
    custom_settings = {
        "ITEM_PIPELINES": {
            "kdramavibe_scrapper.scrapper_spider.scrapper_spider.pipelines.KdramaPipeline": 300,
        }
    }

    def parse(self, response):
        for kdrama in response.css("div.show-recap-detail"):
            kdramaitem = KdramaItem()

            kdramaitem["title"] = kdrama.css("div.show-title-name a::text").get(default="").strip()
            kdramaitem["dramabeans_url"] = kdrama.css("div.show-title-name a::attr(href)").get()
            kdramaitem["rating"] = kdrama.css("div.show-rating span.review-rating::text").get()
            kdramaitem["image_url"] = kdrama.css("div.show-recap-detail-img img::attr(src)").get()
            yield kdramaitem

        # pagination
        next_page = response.css("a.next.page-numbers::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
