import scrapy
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
AJAX_HEADERS = {
    "User-Agent": random.choice(USER_AGENTS),   # from your pool
    "Accept": "text/html, */*; q=0.01",
    "Accept-Language": "en-US,en;q=0.9",
    "X-Requested-With": "XMLHttpRequest",
    "Referer": "https://dramabeans.com",        # often required
    "Connection": "keep-alive",
}
class KactorsSpider(scrapy.Spider):
    name = "kactors"
    allowed_domains = ["dramabeans.com"]
    start_urls = ["https://dramabeans.com/celebs/"]

    custom_settings = {
        "ITEM_PIPELINES": {
            "kdramavibe_scrapper.scrapper_spider.scrapper_spider.pipelines.KactorPipeline": 300,
        }
    }

    def start_requests(self):
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
        for kactor in response.css("div.show-recap-detail"):
            kactoritem = KactorItem()

            kactoritem['name'] = kactor.css("div.show-title-name a::text").get(default="").strip()
            kactoritem["dramabeans_url"] = kactor.css("div.show-title-name a::attr(href)").get()
            kactoritem["image_url"] = kactor.css("div.show-recap-detail-img img::attr(src)").get()
            yield scrapy.Request(
                url=kactoritem['dramabeans_url'],
                callback=self.parse_kactor,
                headers=AJAX_HEADERS,
                meta={"item": kactoritem},
            )

        # pagination
        next_page = response.css("a.next.page-numbers::attr(href)").get()
        if next_page:
            yield response.follow(
                next_page,
                callback=self.parse,
                headers=AJAX_HEADERS
            )

    def parse_kactor(self, response):
        item = response.meta["item"]

        bio_div = response.css("div#bind_tab_bio")
        description_div = response.css("div.banner-description")

        item['name'] = response.css("div.banner-title a h3::text").get().strip() or item['name']
        item['description'] = description_div.xpath("string()").get(default="").strip()
        item['bio'] = bio_div.xpath("string()").get(default="").strip()
        
        item['kdramas'] = response.xpath(
            '//div[@class="banner-type"]//span//a[@class="post_tags"]/text()'
        ).getall()

        birthdays = response.css("p.title-rate::text").getall()
        if birthdays:
            item['birthday'] = birthdays[0].replace("birthday:", "").strip()

        # ✅ Birthplace (first wrapper-user-rating p)
        places = response.css("div.wrapper-user-rating p::text").getall()
        if places:
            item['birthplace'] = places[0].strip()


        yield item

