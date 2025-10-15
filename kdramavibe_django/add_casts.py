# Open Django shell
# python manage.py shell
import os, django
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "kdramavibe_django.settings"
)
django.setup()

from kdramavibe_scrapper.models import Kdrama, Kactor, Krole


# The kdrama slug
kdrama_slug = "boys-over-flowers"
kdrama = Kdrama.objects.get(slug=kdrama_slug)

# Cast data: actor slug -> role_name
cast_data = [
    {"kactor_slug": "koo-hye-sun", "role_name": "Geum Jan-di"},
    {"kactor_slug": "lee-min-ho", "role_name": "Gu Jun-pyo"},
    {"kactor_slug": "kim-hyun-joong", "role_name": "Yoon Ji-hoo"},
    {"kactor_slug": "kim-bum", "role_name": "So Yi-jung"},
    {"kactor_slug": "kim-joon", "role_name": "Song Woo-bin"},
    {"kactor_slug": "ahn-suk-hwan", "role_name": "Geum Il-bong"},
    {"kactor_slug": "im-ye-jin", "role_name": "Na Gong-joo"},
    {"kactor_slug": "kim-so-eun", "role_name": "Chu Ga-eul"},
    {"kactor_slug": "han-chae-young", "role_name": "Min Seo-hyun"},
    {"kactor_slug": "lee-si-young", "role_name": "Oh Min-ji"},
    {"kactor_slug": "kim-hyun-joo", "role_name": "Gu Jun-hee"},
    {"kactor_slug": "lee-hye-young", "role_name": "Kang Hee-soo"},
    {"kactor_slug": "lee-min-jung", "role_name": "Ha Jae-kyung"},
]

for item in cast_data:
    # Lookup actor by slug
    try:
        kactor = Kactor.objects.get(slug=item["kactor_slug"])
    except Kactor.DoesNotExist:
        print(f"Actor with slug '{item['kactor_slug']}' does not exist. Skipping.")
        continue

    # Create the role
    role, created = Krole.objects.get_or_create(
        kdrama=kdrama,
        kactor=kactor,
        role_name=item["role_name"]
    )
    if created:
        print(f"Added role: {item['role_name']} ({kactor.name})")
    else:
        print(f"Role already exists: {item['role_name']} ({kactor.name})")
