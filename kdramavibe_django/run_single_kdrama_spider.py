"""
Run Scrapy spider for a single Kdrama page in Django context.
"""

import os
import django
from scrapy.crawler import CrawlerProcess
from kdramavibe_scrapper.scrapper_spider.scrapper_spider.spiders import SingleKdramaSpider
from kdramavibe_scrapper.models import Kdrama

# Setup Django environment for standalone script
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kdramavibe_django.settings")
django.setup()

# Prompt user for the URL of the Kdrama page to crawl
start_url = input("Enter URL of Kdrama page to crawl: ")

# Initialize Scrapy CrawlerProcess
process = CrawlerProcess()

# Crawl the specified Kdrama page
process.crawl(SingleKdramaSpider, start_url=start_url)
process.start()
