from rest_framework import serializers
from .models import Kdrama, Kactor, Krole

class KdramaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kdrama
        fields = ["title", "start_year", "end_year", "genres", "image_url", "slug"]
    
    

class KactorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kactor
        fields = ["name", "image_url", "slug", "gender", "age"]

class KcastSerializer(serializers.ModelSerializer):
    kactor_name = serializers.CharField(source="kactor.name", read_only=True)
    kactor_slug = serializers.SlugField(source="kactor.slug", read_only=True)

    class Meta:
        model = Krole
        fields = ["role_name", "kactor_name", "kactor_slug"]

from rest_framework import serializers
from .models import Krole

class KactorDramaSerializer(serializers.ModelSerializer):
    kdrama_title = serializers.CharField(source="kdrama.title", read_only=True)
    kdrama_slug = serializers.SlugField(source="kdrama.slug", read_only=True)
    year = serializers.SerializerMethodField()

    class Meta:
        model = Krole
        fields = [
            "kdrama_title",
            "kdrama_slug",
            "role_name",
            "year",
        ]

    def get_year(self, obj):
        start = getattr(obj.kdrama, "start_year", None)
        end = getattr(obj.kdrama, "end_year", None)
        if start and end:
            return f"{start}–{end}" if start != end else str(start)
        elif start:
            return str(start)
        elif end:
            return str(end)
        else:
            return None


class KactorDetailSerializer(serializers.ModelSerializer):
    kdramas = KactorDramaSerializer(source="kactors_roles", many=True, read_only=True)

    class Meta:
        model = Kactor
        exclude = ["id", "created_at", "updated_at"]

class KdramaDetailSerializer(serializers.ModelSerializer):
    kactors = KcastSerializer(source="kdramas_roles", many=True, read_only=True)

    class Meta:
        model = Kdrama
        exclude = ["id", "created_at", "updated_at"]
