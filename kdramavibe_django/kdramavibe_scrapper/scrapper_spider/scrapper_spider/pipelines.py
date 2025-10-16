# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from django.db.models import Q
from kdramavibe_scrapper.models import Kdrama, Kactor, Krole
from asgiref.sync import sync_to_async
from itemadapter import ItemAdapter
from django.utils.text import slugify
from .clean_data import cleaner


class WikipediaKactorPipeline:
    async def process_item(self, item, spider):
        cleaned_item = cleaner.clean_dict(item)
        adapter = ItemAdapter(cleaned_item)

        if adapter.get('name') and adapter.get('wikipedia_url'):
            if adapter.get('image_url') and adapter.get('image_url') == "https:None":
                adapter['image_url'] = None
            await sync_to_async(self.save_or_update_kactor)(adapter)
            return item
  
        else:
            raise ValueError("Kactor name  and wikipedia url required")
        

    def save_or_update_kactor(self, item):
        # Save or update the Kdrama
        wikipedia_url = item.get("wikipedia_url")

        try:
            kactor = Kactor.objects.get(wikipedia_url=wikipedia_url)
            # Update only fields that are not None
            for field, value in item.items():
                if value:
                    setattr(kactor, field, value)
            kactor.save()
        except Kactor.DoesNotExist:
            # Create new actor
            kactor = Kactor.objects.create(
                **item
            )

        return kactor



class WikipediaKdramaPipeline:
    async def process_item(self, item, spider):
        cleaned_item = cleaner.clean_dict(item)
        adapter = ItemAdapter(cleaned_item)

        if adapter.get('title') and adapter.get('wikipedia_url'):
            if adapter.get('image_url') and adapter.get('image_url') == "https:None":
                adapter['image_url'] = None
            await sync_to_async(self.save_or_update_kdrama)(adapter)
            return item
  
        else:
            raise ValueError("Kdrama title and wikipedia url required")
        

    def save_or_update_kdrama(self, item):
        kactors = item.pop('kactors', [])

        # Get existing Kdrama if it exists
        try:
            kdrama = Kdrama.objects.get(wikipedia_url=item["wikipedia_url"])
            # Only update fields that are not None
            for field, value in item.items():
                if value:
                    setattr(kdrama, field, value)
            kdrama.save()
        except Kdrama.DoesNotExist:
            # Create new if not exists
            kdrama = Kdrama.objects.create(**item)

        # Now handle kactors (optional)
        
        for actor_data in kactors:
            actor_name = actor_data.get('actor_name')
            actor_url = actor_data.get('actor_url')

            role_name = actor_data.get('role_name')

            if not actor_name and not actor_url:
                continue

            # Only get or create, no updating
            try:
                kactor = Kactor.objects.get(wikipedia_url=actor_url)
                # Save or update the relationship (Krole)
                Krole.objects.update_or_create(
                    kdrama=kdrama,
                    kactor=kactor,
                    defaults={"role_name": role_name}
                )
            except Kactor.DoesNotExist:
                continue
            
        return kdrama

        



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
            
            if adapter.get('total_rating'):
                adapter['total_rating'] = adapter.get('total_rating').replace("/", "")


            await sync_to_async(self.save_or_update_kdrama)(adapter)
            return item
  
        else:
            raise ValueError("Kdrama title required")
        
    def save_or_update_kdrama(self, item):
        kdrama, _ = Kdrama.objects.update_or_create(
                dramabeans_url=item["dramabeans_url"],
                defaults={
                    "title": item.get("title"),
                    "year": item.get("year"),
                    "image_url": item.get("image_url"),
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
        
class KactorPipeline:
    async def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter.get('name'):
           
            await sync_to_async(self.save_or_update_kactor)(adapter)
            return item
  
        else:
            raise ValueError("Kactor name required")
        
    def save_or_update_kactor(self, item):
        kactor, _ = Kactor.objects.update_or_create(
                dramabeans_url=item["dramabeans_url"],
                defaults={
                    "name": item.get("name"),
                    "image_url": item.get("image_url"),
                    "dramabeans_url": item.get("dramabeans_url"),
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


# class KdramaPipeline:
#     async def process_item(self, item, spider):
#         adapter = ItemAdapter(item)

#         if adapter.get('title'):
#             title_year = adapter.get('title')
#             if " (" in title_year:
#                 title, year = title_year.rsplit(" (", 1)
#                 year = year.replace(")", "")
#                 adapter['year'] = year
#                 adapter['title'] = title
           
#             else:
#                 title, year = title_year, None
            
#             if adapter.get('total_rating'):
#                 adapter['total_rating'] = adapter.get('total_rating').replace("/", "")


#             await sync_to_async(self.save_kdrama)(adapter)
#             return item
  
#         else:
#             raise ValueError("Kdrama title required")
        
#     def save_kdrama(self, item):
#         kdrama, _ = Kdrama.objects.update_or_create(
#                 dramabeans_url=item["dramabeans_url"],
#                 defaults={
#                     "title": item.get("title"),
#                     "year": item.get("year"),
#                     "rating": item.get("rating"),
#                     "image_url": item.get("image_url"),
#                     "dramabeans_url": item.get("dramabeans_url"),

#                 }
#             )
        
#         return kdrama
        


# class KactorPipeline:
#     async def process_item(self, item, spider):
#         adapter = ItemAdapter(item)

#         if adapter.get('name'):
#             await sync_to_async(self.save_kactor)(adapter)
#             return item
  
#         else:
#             raise ValueError("Kactor name required")
        

#     def save_kactor(self, item):
#         kactor, _ = Kactor.objects.update_or_create(
#             dramabeans_url=item["dramabeans_url"],
#             defaults={
#                 "name": item.get("name"),
#                 "image_url": item.get("image_url"),
#                 "dramabeans_url": item.get("dramabeans_url"),
#             }
#         )

#         return kactor