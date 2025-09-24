import scrapy
from ..items import KdramaItem

import scrapy
from ..items import KdramaItem

class KdramaDetailsSpider(scrapy.Spider):
    name = "kdrama_details"
    allowed_domains = ["dramabeans.com"]
    start_urls = ["https://dramabeans.com/shows/autumn-fairy-tale/"]
    custom_settings = {
        "ITEM_PIPELINES": {
            "kdramavibe_scrapper.scrapper_spider.scrapper_spider.pipelines.KdramaDetailsPipeline": 300,
        }
    }

    # def __init__(self, url = None, *args, **kwargs):
        #     super(KdramaDetailsSpider, self).__init__(*args, **kwargs)
        #     self.start_urls = [url] if url else []

    def parse(self, response):
        kdramaitem = KdramaItem()

        kdramaitem['title'] = response.css('div.banner-title a h3::text').get()
        rating = response.css('div.banner-title-rate span.rating::text').get()
        total_rating = response.css('div.banner-title-rate span.total-rating::text').get()
        kdramaitem['rating'] = f"{rating} {total_rating}"        
        kdramaitem['description'] = response.css('div.banner-description p::text').get()
        kdramaitem['genre'] = response.xpath('//div[@class="banner-type"]//span//a[@class="post_tags"]/text()').getall()

        kactors_list = []
       
        for kactor in response.css('#show_casts .casts-detail'):
            name = kactor.css('.casts-name a::text').get()
            role = kactor.css('.casts-character-name::text').get()
            dramabeans_url = kactor.css('.casts-name a::attr(href)').get()

            if name and role:
                kactors_list.append({
                    'name': name.strip(),
                    'role': role.strip(),
                    'dramabeans_url': dramabeans_url
                })

        kdramaitem['kactors'] = kactors_list


        yield kdramaitem

