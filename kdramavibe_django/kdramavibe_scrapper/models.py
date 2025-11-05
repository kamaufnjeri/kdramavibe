from django.db import models
from uuid import uuid4
from django.utils.text import slugify


class BaseModel(models.Model):
    """
    Abstract base model providing UUID primary key and timestamp fields.
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid4,
        editable=False
    )
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when created
    updated_at = models.DateTimeField(auto_now=True)      # Timestamp when last updated

    class Meta:
        abstract = True  # Prevents creation of a separate database table


class Kdrama(BaseModel):
    """
    Model representing a Kdrama with related metadata.
    """
    title = models.CharField(max_length=255)
    start_year = models.CharField(max_length=10, blank=True, null=True)
    end_year = models.CharField(max_length=10, blank=True, null=True)
    plot = models.TextField(blank=True, null=True)
    writers = models.JSONField(blank=True, null=True)
    languages = models.JSONField(blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    directors = models.JSONField(blank=True, null=True)
    wikipedia_url = models.URLField(unique=True)
    image_url = models.URLField(max_length=500, blank=True, null=True)
    alternate_titles = models.JSONField(blank=True, null=True)
    genres = models.JSONField(blank=True, null=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    episodes = models.JSONField(blank=True, null=True)
    seasons = models.CharField(max_length=10, blank=True, null=True)
    networks = models.JSONField(blank=True, null=True)
    running_time = models.CharField(max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        """
        Automatically generate a unique slug from the title if not provided.
        """
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Kdrama.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Kactor(BaseModel):
    """
    Model representing a Kactor with related metadata.
    """
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female')
    ]

    name = models.CharField(max_length=255)
    alternate_names = models.JSONField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, null=True, blank=True)
    birthday = models.DateField(blank=True, null=True)
    birthplace = models.CharField(max_length=255, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    occupations = models.JSONField(blank=True, null=True)
    children = models.JSONField(blank=True, null=True)
    years_active = models.CharField(max_length=255, blank=True, null=True)
    agents = models.JSONField(blank=True, null=True)
    height = models.CharField(max_length=50, blank=True, null=True)
    partner_or_spouse = models.CharField(max_length=255, blank=True, null=True)
    wikipedia_url = models.URLField(unique=True, blank=True, null=True)
    image_url = models.URLField(max_length=500, blank=True, null=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    kdramas = models.ManyToManyField('Kdrama', through='Krole')  # Many-to-many relationship through Krole
    dramabeans_url = models.URLField(unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        """
        Automatically generate a unique slug from the name if not provided.
        """
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Kactor.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Krole(BaseModel):
    """
    Through model representing a Kactor's role in a Kdrama.
    """
    kactor = models.ForeignKey(
        Kactor, related_name="kactors_roles", on_delete=models.CASCADE
    )
    kdrama = models.ForeignKey(
        Kdrama, related_name="kdramas_roles", on_delete=models.CASCADE
    )
    role_name = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.kactor.name} as {self.role_name} in {self.kdrama.title}"


class DramabeansKdrama(BaseModel):
    """
    Model representing Kdrama data from Dramabeans source.
    """
    title = models.CharField(max_length=255)
    year = models.CharField(max_length=10, blank=True, null=True)
    rating = models.FloatField(blank=True, null=True)
    no_of_votes = models.FloatField(blank=True, null=True)
    dramabeans_url = models.URLField(unique=True, blank=True, null=True)
    kdrama = models.OneToOneField(
        Kdrama,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name="dramabeans_details",
    )


class DramabeansKactor(BaseModel):
    """
    Model representing Kactor data from Dramabeans source.
    """
    name = models.CharField(max_length=255)
    image_url = models.URLField(max_length=500, blank=True, null=True)
    no_of_votes = models.FloatField(blank=True, null=True)
    dramabeans_url = models.URLField(unique=True, blank=True, null=True)
    birthday = models.DateField(max_length=255, blank=True, null=True)
    birthplace = models.CharField(max_length=255, blank=True, null=True)
    kactor = models.OneToOneField(
        Kactor,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name="dramabeans_details",
    )
