"""
Run Scrapy spider to crawl Wikipedia Kdramas pages in Django context.
"""

import os
import django
from scrapy.crawler import CrawlerProcess
from kdramavibe_scrapper.scrapper_spider.scrapper_spider.spiders import WikipediaKdramasSpider
from kdramavibe_scrapper.models import Kdrama

# Setup Django environment for standalone script
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kdramavibe_django.settings")
django.setup()

# Initialize Scrapy CrawlerProcess
process = CrawlerProcess()

# Crawl Wikipedia Kdramas pages
process.crawl(WikipediaKdramasSpider)
process.start()
