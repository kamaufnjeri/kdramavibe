import scrapy
from urllib.parse import quote
from ..items import KactorItem


class KactorDetailsSpider(scrapy.Spider):
    name = "kactor_details"
    allowed_domains = ["dramabeans.com"]

    def __init__(self, dramabeans_url=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not dramabeans_url:
            raise ValueError("Dramabeans url is needed")
        self.start_urls = [dramabeans_url]
        
    custom_settings = {
        "ITEM_PIPELINES": {
            "kdramavibe_scrapper.scrapper_spider.scrapper_spider.pipelines.KactorDetailsPipeline": 300,
        }
    }

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
