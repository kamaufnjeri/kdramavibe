"""
Run Scrapy spiders for Kactor data collection in Django context.
"""

import os
import django
from scrapy.crawler import CrawlerProcess
from kdramavibe_scrapper.scrapper_spider.scrapper_spider.spiders import KactorsSpider
from kdramavibe_scrapper.models import Kactor

# Setup Django environment for standalone script
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kdramavibe_django.settings")
django.setup()

# Initialize Scrapy CrawlerProcess
process = CrawlerProcess()

# Crawl KactorsSpider to gather all Kactor data
process.crawl(KactorsSpider)
process.start()


# # Optional: Pull Kactors with existing Dramabeans URLs
# kactors = list(
#     Kactor.objects
#     .exclude(dramabeans_url__isnull=True)   # exclude NULL URLs
#     .exclude(dramabeans_url="")             # exclude empty string URLs
#     .values_list("name", "dramabeans_url")
# )

# # Example: crawl details for Kactors with existing Dramabeans URLs
# process = CrawlerProcess()
# process.crawl(KactorDetailsSpider, kactors=kactors)
# process.start()
