# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from django.db.models import Q
from kdramavibe_scrapper.models import Kdrama, Kactor, Krole, DramabeansKdrama, DramabeansKactor
from asgiref.sync import sync_to_async
from itemadapter import ItemAdapter
from django.utils.text import slugify
from .clean_data import cleaner


class WikipediaKactorPipeline:
    """
    Pipeline to process Wikipedia Kactor items and save them to Django models.
    """

    async def process_item(self, item, spider):
        """
        Async processing of each Kactor item.
        Cleans the item and saves or updates it in the database.
        """
        cleaned_item = cleaner.clean_dict(item)
        adapter = ItemAdapter(cleaned_item)

        if adapter.get("name") and adapter.get("wikipedia_url"):
            # Handle invalid image URLs
            if adapter.get("image_url") and adapter.get("image_url") == "https:None":
                adapter["image_url"] = None
            await sync_to_async(self.save_or_update_kactor)(adapter)
            return item
        else:
            raise ValueError("Kactor name and wikipedia url required")

    def save_or_update_kactor(self, item):
        """
        Saves a new Kactor or updates existing one based on wikipedia_url.
        """
        wikipedia_url = item.get("wikipedia_url")

        try:
            kactor = Kactor.objects.get(wikipedia_url=wikipedia_url)
            # Update only fields that are not None
            for field, value in item.items():
                if value:
                    setattr(kactor, field, value)
            kactor.save()
        except Kactor.DoesNotExist:
            # Create new actor if not found
            kactor = Kactor.objects.create(**item)

        return kactor


class WikipediaKdramaPipeline:
    """
    Pipeline to process Wikipedia Kdrama items and save them to Django models.
    """

    async def process_item(self, item, spider):
        """
        Async processing of each Kdrama item.
        Cleans the item and saves or updates it in the database.
        """
        cleaned_item = cleaner.clean_dict(item)
        adapter = ItemAdapter(cleaned_item)

        if adapter.get("title") and adapter.get("wikipedia_url"):
            # Handle invalid image URLs
            if adapter.get("image_url") and adapter.get("image_url") == "https:None":
                adapter["image_url"] = None
            await sync_to_async(self.save_or_update_kdrama)(adapter)
            return item
        else:
            raise ValueError("Kdrama title and wikipedia url required")

    def save_or_update_kdrama(self, item):
        """
        Saves or updates Kdrama and its actors (Kactors and Kroles).
        """
        kactors = item.pop("kactors", [])

        # Get existing Kdrama if it exists
        try:
            kdrama = Kdrama.objects.get(wikipedia_url=item["wikipedia_url"])
            for field, value in item.items():
                if value:
                    setattr(kdrama, field, value)
            kdrama.save()
        except Kdrama.DoesNotExist:
            # Create new if not exists
            kdrama = Kdrama.objects.create(**item)

        # Handle kactors
        for actor_data in kactors:
            actor_name = actor_data.get("actor_name")
            actor_url = actor_data.get("actor_url")
            role_name = actor_data.get("role_name")

            if not actor_name and not actor_url:
                continue

            try:
                kactor = Kactor.objects.get(wikipedia_url=actor_url)
                # Save or update the relationship (Krole)
                Krole.objects.update_or_create(
                    kdrama=kdrama, kactor=kactor, defaults={"role_name": role_name}
                )
            except Kactor.DoesNotExist:
                continue

        return kdrama


class KdramaPipeline:
    """
    Pipeline to process DramaBeans Kdrama items and save them to Django models.
    """

    async def process_item(self, item, spider):
        """
        Async processing of each Kdrama item.
        Extracts title and year and saves or updates in the database.
        """
        adapter = ItemAdapter(item)

        if adapter.get("title"):
            title_year = adapter.get("title")
            # Split title and year if present
            if " (" in title_year:
                title, year = title_year.rsplit(" (", 1)
                year = year.replace(")", "")
                adapter["year"] = year
                adapter["title"] = title
            else:
                title, year = title_year, None

            await sync_to_async(self.save_or_update_kdrama)(adapter)
            return item
        else:
            raise ValueError("Kdrama title required")

    def save_or_update_kdrama(self, item):
        """
        Saves or updates a Kdrama entry in DramabeansKdrama table.
        """
        kdrama, _ = DramabeansKdrama.objects.update_or_create(
            dramabeans_url=item["dramabeans_url"],
            defaults={
                "title": item.get("title"),
                "year": item.get("year"),
                "rating": item.get("rating"),
                "no_of_votes": item.get("no_of_votes"),
                "dramabeans_url": item.get("dramabeans_url"),
            },
        )
        return kdrama


class KactorPipeline:
    """
    Pipeline to process DramaBeans Kactor items and save them to Django models.
    """

    async def process_item(self, item, spider):
        """
        Async processing of each Kactor item.
        Saves or updates in the database.
        """
        adapter = ItemAdapter(item)

        if adapter.get("name"):
            await sync_to_async(self.save_or_update_kactor)(adapter)
            return item
        else:
            raise ValueError("Kactor name required")

    def save_or_update_kactor(self, item):
        """
        Saves or updates a Kactor entry in DramabeansKactor table.
        """
        kactor, _ = DramabeansKactor.objects.update_or_create(
            dramabeans_url=item["dramabeans_url"],
            defaults={
                "name": item.get("name"),
                "image_url": item.get("image_url"),
                "birthday": item.get("birthday"),
                "birthplace": item.get("birthplace"),
                "dramabeans_url": item.get("dramabeans_url"),
                "no_of_votes": item.get("no_of_votes"),
            },
        )
        return kactor


# --------------------------
# Legacy commented pipelines
# --------------------------

# class KdramaPipeline:
#     async def process_item(self, item, spider):
#         adapter = ItemAdapter(item)
#
#         if adapter.get('title'):
#             title_year = adapter.get('title')
#             if " (" in title_year:
#                 title, year = title_year.rsplit(" (", 1)
#                 year = year.replace(")", "")
#                 adapter['year'] = year
#                 adapter['title'] = title
#             else:
#                 title, year = title_year, None
#
#             if adapter.get('total_rating'):
#                 adapter['total_rating'] = adapter.get('total_rating').replace("/", "")
#
#             await sync_to_async(self.save_kdrama)(adapter)
#             return item
#         else:
#             raise ValueError("Kdrama title required")
#
#     def save_kdrama(self, item):
#         kdrama, _ = Kdrama.objects.update_or_create(
#             dramabeans_url=item["dramabeans_url"],
#             defaults={
#                 "title": item.get("title"),
#                 "year": item.get("year"),
#                 "rating": item.get("rating"),
#                 "image_url": item.get("image_url"),
#                 "dramabeans_url": item.get("dramabeans_url"),
#             }
#         )
#         return kdrama
#
#
# class KactorPipeline:
#     async def process_item(self, item, spider):
#         adapter = ItemAdapter(item)
#         if adapter.get('name'):
#             await sync_to_async(self.save_kactor)(adapter)
#             return item
#         else:
#             raise ValueError("Kactor name required")
#
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
