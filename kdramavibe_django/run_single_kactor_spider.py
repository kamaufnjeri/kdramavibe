"""
Run Scrapy spider for a single Kactor page in Django context.
"""

import os
import django
from scrapy.crawler import CrawlerProcess
from kdramavibe_scrapper.scrapper_spider.scrapper_spider.spiders import SingleKactorSpider

# Setup Django environment for standalone script
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kdramavibe_django.settings")
django.setup()

# Prompt user for the URL of the Kactor page to crawl
start_url = input("Enter URL of Kactor page to crawl: ")

# Initialize Scrapy CrawlerProcess
process = CrawlerProcess()

# Crawl the specified Kactor page
process.crawl(SingleKactorSpider, start_url=start_url)
process.start()
