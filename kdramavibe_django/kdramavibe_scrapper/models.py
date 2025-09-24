from django.db import models
from uuid import uuid4
from django.utils.text import slugify

# Base model with UUID and timestamps
class BaseModel(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid4,
        editable=False
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True  # prevents BaseModel from creating its own table


class Kdrama(BaseModel):
    title = models.CharField(max_length=255)
    year = models.CharField(max_length=10, blank=True, null=True)
    rating = models.FloatField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    writers = models.JSONField(blank=True, null=True)
    directors = models.JSONField(blank=True, null=True)
    dramabeans_url = models.URLField(unique=True, blank=True, null=True)
    wikipedia_url = models.URLField(unique=True, blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    alternate_titles = models.JSONField(blank=True, null=True)
    genre = models.JSONField(blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True)
    episodes = models.IntegerField(blank=True, null=True)
    network = models.CharField(max_length=255, blank=True, null=True)
    release_date = models.CharField(blank=True, null=True)
    running_time = models.CharField(max_length=50, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Kactor(BaseModel):
    name = models.CharField(max_length=255)
    alternate_names = models.JSONField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    education = models.JSONField(blank=True, null=True)       
    occupations = models.JSONField(blank=True, null=True)      
    years_active = models.CharField(max_length=50, blank=True, null=True)  
    agent = models.CharField(max_length=255, blank=True, null=True)
    height = models.CharField(max_length=50, blank=True, null=True)  
    partner_or_spouse = models.CharField(max_length=255, blank=True, null=True)
    dramabeans_url = models.URLField(unique=True, blank=True, null=True)
    wikipedia_url = models.URLField(unique=True, blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)

    slug = models.SlugField(unique=True, blank=True)
    kdramas = models.ManyToManyField('Kdrama', through='Krole')


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Krole(BaseModel):
    kactor = models.ForeignKey(Kactor, on_delete=models.CASCADE)
    kdrama = models.ForeignKey(Kdrama, on_delete=models.CASCADE)
    role_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.actor.name} as {self.role_name} in {self.drama.title}"
