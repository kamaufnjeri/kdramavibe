import scrapy
from ..items import KactorItem

class KactorsSpider(scrapy.Spider):
    name = "kactors"
    allowed_domains = ["dramabeans.com"]
    start_urls = ["https://dramabeans.com/celebs/"]

    custom_settings = {
        "ITEM_PIPELINES": {
            "kdramavibe_scrapper.scrapper_spider.scrapper_spider.pipelines.KactorPipeline": 300,
        }
    }

    def parse(self, response):
        for kactor in response.css("div.show-recap-detail"):
            kactoritem = KactorItem()

            kactoritem['name'] = kactor.css("div.show-title-name a::text").get(default="").strip()
            kactoritem["dramabeans_url"] = kactor.css("div.show-title-name a::attr(href)").get()
            kactoritem["image_url"] = kactor.css("div.show-recap-detail-img img::attr(src)").get()
            yield kactoritem

        # pagination
        next_page = response.css("a.next.page-numbers::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
