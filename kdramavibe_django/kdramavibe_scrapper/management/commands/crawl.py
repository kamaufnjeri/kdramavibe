import os
from django.core.management.base import BaseCommand
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from kdramavibe_scrapper.scrapper_spider.scrapper_spider.spiders import (
    KactorsSpider,
    KdramasSpider,
    KdramaDetailsSpider,
    KactorDetailsSpider,
)
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
        parser.add_argument(
            "-a",
            "--spargs",
            dest="spargs",
            action="append",
            default=[],
            help="Spider arguments (key=value)",
        )

    def handle(self, *args, **options):
        spider_name = options["spider"]

        # Map spider names to their classes
        spiders = {
            "kdramas": KdramasSpider,
            "kactors": KactorsSpider,
            "kdrama_details": KdramaDetailsSpider,
            "kactor_details": KactorDetailsSpider,
        }

        if spider_name not in spiders:
            self.stdout.write(
                self.style.ERROR(
                    f"Unknown spider: {spider_name}. Available: {', '.join(spiders.keys())}"
                )
            )
            return

        # Convert -a arguments ["key=value", "foo=bar"] → {"key":"value", "foo":"bar"}
        spargs = {}
        for arg in options["spargs"]:
            if "=" in arg:
                k, v = arg.split("=", 1)
                spargs[k] = v

        settings = Settings()
        settings.setmodule(project_settings)

        process = CrawlerProcess(settings)
        # ✅ forward the spargs here
        process.crawl(spiders[spider_name], **spargs)
        process.start()

        self.stdout.write(
            self.style.SUCCESS(f"Spider '{spider_name}' finished successfully!")
        )
