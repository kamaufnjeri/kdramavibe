import os, django
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "kdramavibe_django.settings"
)
django.setup()
from scrapy.crawler import CrawlerProcess
from kdramavibe_scrapper.scrapper_spider.scrapper_spider.spiders import (
    KactorDetailsSpider,
)
from kdramavibe_scrapper.models import Kactor



# Pull the list of kactors with dramabeans URLs
kactors = list(
    Kactor.objects
    .exclude(dramabeans_url__isnull=True)       # exclude NULL
    .exclude(dramabeans_url="")                 # exclude empty strings
    .values_list("name", "dramabeans_url")
)

process = CrawlerProcess()
process.crawl(KactorDetailsSpider, kactors=kactors)
process.start()
