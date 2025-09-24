from rest_framework import serializers
from .models import Kdrama, Kactor

class KdramaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kdrama
        fields = ["title", "year", "rating", "image_url", "slug"]

class KactorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kdrama
        fields = ["name", "image_url", "rating", "slug"]
