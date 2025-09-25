import scrapy
from urllib.parse import quote
from ..items import KdramaItem


class KdramaDetailsSpider(scrapy.Spider):
    name = "kdrama_details"
    allowed_domains = ["dramabeans.com"]


    def __init__(self, dramabeans_url=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not dramabeans_url:
            raise ValueError("Dramabeans url is needed")
        self.start_urls = [dramabeans_url]

    custom_settings = {
        "ITEM_PIPELINES": {
            "kdramavibe_scrapper.scrapper_spider.scrapper_spider.pipelines.KdramaDetailsPipeline": 300,
        }
    }

    def parse(self, response):
        """Parse main show page details and schedule AJAX call for casts."""
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

        # Extract show_id from page (in HTML attrs or URL)
        show_id = response.css("input#show_id::attr(value)").get()


        # Build AJAX URL for casts
        title = item['title'] or "Unknown"
        ajax_url = (
            "https://dramabeans.com/casts/"
            f"?show_id={show_id}&tag={quote(title)}&order=desc&shows=shows&select_ajax=select_ajax"
        )

        # Pass item forward to next parser
        yield scrapy.Request(
            url=ajax_url,
            callback=self.parse_casts,
            meta={"item": item},
        )

    def parse_casts(self, response):
        """Parse the AJAX-loaded cast list and attach to item."""
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
