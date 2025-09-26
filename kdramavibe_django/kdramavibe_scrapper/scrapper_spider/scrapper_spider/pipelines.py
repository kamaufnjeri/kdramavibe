# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from kdramavibe_scrapper.models import Kdrama, Kactor, Krole
from asgiref.sync import sync_to_async
from itemadapter import ItemAdapter
from django.utils.text import slugify


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
        kdrama, _ = Kdrama.objects.update_or_create(
                dramabeans_url=item["dramabeans_url"],
                defaults={
                    "title": item.get("title"),
                    "year": item.get("year"),
                    "rating": item.get("rating"),
                    "image_url": item.get("image_url"),
                    "dramabeans_url": item.get("dramabeans_url"),

                }
            )
        
        return kdrama
        


class KactorPipeline:
    async def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        if adapter.get('name'):
            await sync_to_async(self.save_kactor)(adapter)
            return item
  
        else:
            raise ValueError("Kactor name required")
        

    def save_kactor(self, item):
        kactor, _ = Kactor.objects.update_or_create(
            dramabeans_url=item["dramabeans_url"],
            defaults={
                "name": item.get("name"),
                "image_url": item.get("image_url"),
                "dramabeans_url": item.get("dramabeans_url"),
            }
        )

        return kactor


class KdramaDetailsPipeline:
    async def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        if adapter.get('dramabeans_url'):
            if adapter.get('total_rating'):
                adapter['total_rating'] = adapter.get('total_rating').replace("/", "")
            await sync_to_async(self.update_kdrama)(adapter)
            return item
  
        else:
            raise ValueError("dramabeans url required")
        
    def update_kdrama(self, item):
        kdrama, _ = Kdrama.objects.update_or_create(
                dramabeans_url=item["dramabeans_url"],
                defaults={
                    "title": item.get("title"),
                    "description": item.get("description"),
                    "rating": item.get("rating"),
                    "total_rating": item.get("total_rating"),
                    "genre": item.get("genre"),
                    "dramabeans_url": item.get("dramabeans_url"),
                }
            )
        for actor_data in item.get('kactors', []):
            kactor, _ = Kactor.objects.get_or_create(
                dramabeans_url=actor_data['dramabeans_url'],
                defaults={'name': actor_data['name'], "dramabeans_url": item.get("dramabeans_url"),
}
            )

            # Link via KRole (avoid duplicates)
            Krole.objects.update_or_create(
                kdrama=kdrama,
                kactor=kactor,
                defaults={'role_name': actor_data['role']}
            )
        
        return kdrama
        
class KactorDetailsPipeline:
    async def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter.get('dramabeans_url'):
           
            await sync_to_async(self.update_kactor)(adapter)
            return item
  
        else:
            raise ValueError("dramabeans url required")
        
    def update_kactor(self, item):
        kactor, _ = Kactor.objects.update_or_create(
                dramabeans_url=item["dramabeans_url"],
                defaults={
                    "name": item.get("name"),
                    "description": item.get("description"),
                    "bio": item.get("bio"),
                    "birthday": item.get("birthday"),
                    "birthplace": item.get("birthplace"),
                    "dramabeans_url": item.get("dramabeans_url"),
                }
            )
        for kdrama_title in item.get('kdramas', []):
            slug = slugify(kdrama_title.strip())
            kdrama, _ = Kdrama.objects.get_or_create(
                slug=slug,
                defaults={'title': kdrama_title.strip() },

            )

            # Link via KRole (avoid duplicates)
            Krole.objects.update_or_create(
                kdrama=kdrama,
                kactor=kactor
            )
        
        return kactor
