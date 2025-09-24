import os
from django.core.management.base import BaseCommand
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from kdramavibe_scrapper.scrapper_spider.scrapper_spider.spiders import KactorsSpider, KdramasSpider, KdramaDetailsSpider
from kdramavibe_scrapper.scrapper_spider.scrapper_spider import settings as project_settings

print(project_settings.BOT_NAME)

class Command(BaseCommand):
    help = "Run a scrapy spider from Django"

    
    def add_arguments(self, parser):
        parser.add_argument(
            "spider",
            type=str,
            help="The spider name (e.g. kdramas, kactors)",
        )

    def handle(self, *args, **options):
        spider_name = options["spider"]

        # Map spider names to their classes
        spiders = {
            "kdramas": KdramasSpider,
            "kactors": KactorsSpider,
            "kdrama_details": KdramaDetailsSpider
        }

        if spider_name not in spiders:
            self.stdout.write(self.style.ERROR(
                f"Unknown spider: {spider_name}. Available: {', '.join(spiders.keys())}"
            ))
            return
        
        settings = Settings()
        settings.setmodule(project_settings)
        process = CrawlerProcess(settings)
        process.crawl(spiders[spider_name])
        process.start()

        self.stdout.write(self.style.SUCCESS(f"Spider '{spider_name}' finished successfully!"))