"""
Run Scrapy spiders for Kdrama data collection in Django context.
"""

import os
import django
from scrapy.crawler import CrawlerProcess
from kdramavibe_scrapper.scrapper_spider.scrapper_spider.spiders import KdramasSpider
from kdramavibe_scrapper.models import Kdrama

# Setup Django environment for standalone script
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kdramavibe_django.settings")
django.setup()

# Initialize Scrapy CrawlerProcess
process = CrawlerProcess()

# Crawl KdramasSpider to gather all Kdrama data
process.crawl(KdramasSpider)
process.start()


# # Optional: Pull Kdramas with existing Dramabeans URLs
# kdramas = list(
#     Kdrama.objects
#     .exclude(dramabeans_url__isnull=True)   # exclude NULL URLs
#     .exclude(dramabeans_url="")             # exclude empty string URLs
#     .values_list("title", "dramabeans_url")
# )

# # Example: crawl details for Kdramas with existing Dramabeans URLs
# process = CrawlerProcess()
# process.crawl(KdramaDetailsSpider, kdramas=kdramas)
# process.start()
