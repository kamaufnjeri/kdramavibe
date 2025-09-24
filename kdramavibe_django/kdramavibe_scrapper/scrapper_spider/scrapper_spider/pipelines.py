# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from kdramavibe_scrapper.models import Kdrama, Kactor, Krole
from asgiref.sync import sync_to_async
from itemadapter import ItemAdapter


class KdramaPipeline:
    async def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        if adapter.get('title'):
            title_year = adapter.get('title')
            if " (" in title_year:
                title, year = title_year.rsplit(" (", 1)
                year = year.replace(")", "")
                adapter['year'] = year
                adapter['title'] = title

            else:
                title, year = title_year, None

            await sync_to_async(self.save_kdrama)(adapter)
            return item
  
        else:
            raise ValueError("Kdrama title required")
        
    def save_kdrama(self, item):
        obj, created = Kdrama.objects.update_or_create(
                dramabeans_url=item["dramabeans_url"],
                defaults={
                    "title": item.get("title"),
                    "year": item.get("year"),
                    "rating": item.get("rating"),
                    "image_url": item.get("image_url"),
                    "dramabeans_url": item.get("dramabeans_url"),

                }
            )
        
        return obj
        


class KactorPipeline:
    async def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        if adapter.get('name'):
            await sync_to_async(self.save_kactor)(adapter)
            return item
  
        else:
            raise ValueError("Kactor name required")
        

    def save_kactor(self, item):
        obj, created = Kactor.objects.update_or_create(
            dramabeans_url=item["dramabeans_url"],
            defaults={
                "name": item.get("name"),
                "image_url": item.get("image_url"),
                "dramabeans_url": item.get("dramabeans_url"),
            }
        )

        return obj


class KdramaDetailsPipeline:
    def process_item(self, item, spider):
        return item