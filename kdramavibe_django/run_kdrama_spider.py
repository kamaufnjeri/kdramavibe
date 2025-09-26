import os, django
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "kdramavibe_django.settings"
)
django.setup()
from scrapy.crawler import CrawlerProcess
from kdramavibe_scrapper.scrapper_spider.scrapper_spider.spiders import (
    KdramaDetailsSpider,
)
from kdramavibe_scrapper.models import Kdrama



# Pull the list of kdramas with dramabeans URLs
kdramas = list(
    Kdrama.objects
    .exclude(dramabeans_url__isnull=True)       # exclude NULL
    .exclude(dramabeans_url="")                 # exclude empty strings
    .values_list("title", "dramabeans_url")
)

process = CrawlerProcess()
process.crawl(KdramaDetailsSpider, kdramas=kdramas)
process.start()
