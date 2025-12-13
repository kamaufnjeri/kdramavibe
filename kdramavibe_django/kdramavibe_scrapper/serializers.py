from rest_framework import serializers
from .models import Kdrama, Kactor, Krole, DramabeansKdrama


class KdramaSerializer(serializers.ModelSerializer):
    """
    Serializer for Kdrama model with additional fields from Dramabeans.
    """
    rating = serializers.CharField(
        source="dramabeans_details.rating", read_only=True
    )
    no_of_votes = serializers.CharField(
        source="dramabeans_details.no_of_votes", read_only=True
    )

    class Meta:
        model = Kdrama
        fields = [
            "title",
            "start_year",
            "end_year",
            "genres",
            "image_url",
            "slug",
            "rating",
            "no_of_votes",
        ]


class KactorSerializer(serializers.ModelSerializer):
    """
    Serializer for Kactor model with Dramabeans votes and image URL.
    """
    no_of_votes = serializers.CharField(
        source="dramabeans_details.no_of_votes", read_only=True
    )
    dramabeans_image_url = serializers.CharField(
        source="dramabeans_details.image_url", read_only=True
    )

    class Meta:
        model = Kactor
        fields = [
            "name",
            "image_url",
            "slug",
            "gender",
            "age",
            "no_of_votes",
            "dramabeans_image_url",
        ]


class KcastSerializer(serializers.ModelSerializer):
    """
    Serializer for Krole to expose actor details in a Kdrama.
    """
    kactor_name = serializers.CharField(source="kactor.name", read_only=True)
    kactor_slug = serializers.SlugField(source="kactor.slug", read_only=True)
    kactor_gender = serializers.CharField(source="kactor.gender", read_only=True)
    kactor_image_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Krole
        fields = [
            "role_name",
            "kactor_name",
            "kactor_slug",
            "kactor_image_url",
            "kactor_gender",
        ]

    def get_kactor_image_url(self, obj):
        """
        Return the image URL from Kactor or fallback to Dramabeans image.
        """
        if obj.kactor.image_url:
            return obj.kactor.image_url

        dramabeans_details = getattr(obj.kactor, "dramabeans_details", None)
        if dramabeans_details and getattr(dramabeans_details, "image_url", None):
            return dramabeans_details.image_url

        return None


class KactorDramaSerializer(serializers.ModelSerializer):
    """
    Serializer to show a Kactor's roles in Kdramas.
    """
    kdrama_title = serializers.CharField(source="kdrama.title", read_only=True)
    kdrama_slug = serializers.SlugField(source="kdrama.slug", read_only=True)
    kdrama_image_url = serializers.SerializerMethodField(read_only=True)
    year = serializers.SerializerMethodField()

    class Meta:
        model = Krole
        fields = ["kdrama_title", "kdrama_slug", "role_name", "year", "kdrama_image_url"]

    def get_year(self, obj):
        """
        Return formatted start–end years of the drama.
        """
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
    def get_kdrama_image_url(self, obj):
        """
        Return the image URL from Kactor or fallback to Dramabeans image.
        """
        if obj.kdrama.image_url:
            return obj.kdrama.image_url

        dramabeans_details = getattr(obj.kdrama, "dramabeans_details", None)
        if dramabeans_details and getattr(dramabeans_details, "image_url", None):
            return dramabeans_details.image_url

        return None

class KactorDetailSerializer(KactorSerializer):
    """
    Detailed Kactor serializer including Kdramas.
    """
    kdramas = serializers.SerializerMethodField(read_only=True)
    dramabeans_url = serializers.CharField(
        source="dramabeans_details.dramabeans_url", read_only=True
    )

    class Meta:
        model = Kactor
        exclude = ["id", "created_at", "updated_at"]

    def get_kdramas(self, obj):
        """
        Return dramas ordered by start_year then end_year.
        """
        roles = (
            obj.kactors_roles.all()
            .select_related("kdrama")
            .order_by("-kdrama__start_year", "-kdrama__end_year")
        )
        return KactorDramaSerializer(roles, many=True, context=self.context).data


class KdramaDetailSerializer(KdramaSerializer):
    """
    Detailed Kdrama serializer including cast and Dramabeans URL.
    """
    dramabeans_url = serializers.CharField(
        source="dramabeans_details.dramabeans_url", read_only=True
    )
    kactors = KcastSerializer(source="kdramas_roles", many=True, read_only=True)

    class Meta:
        model = Kdrama
        exclude = ["id", "created_at", "updated_at"]


# Serializers for matching and linking/unlinking

class KdramaMatchSerializer(serializers.Serializer):
    """
    Serializer for Kdrama comparison results.
    """
    dramabeans_id = serializers.UUIDField()
    wiki_id = serializers.UUIDField()
    dramabeans_title = serializers.CharField()
    wiki_title = serializers.CharField()
    alternate_titles = serializers.ListField()
    best_score = serializers.FloatField()
    start_year = serializers.CharField()
    end_year = serializers.CharField()
    dramabeans_year = serializers.CharField()
    years_match = serializers.BooleanField()
    is_match = serializers.BooleanField()


# class LinkKdramasSerializer(serializers.Serializer):
#     """Serializer to link Dramabeans Kdrama to a Wiki Kdrama."""
#     dramabeans_id = serializers.UUIDField()
#     kdrama_id = serializers.UUIDField()


# class UnlinkKdramasSerializer(serializers.Serializer):
#     """Serializer to unlink one or more Dramabeans Kdramas."""
#     dramabeans_ids = serializers.ListField(
#         child=serializers.UUIDField(), allow_empty=False
#     )


class KactorMatchSerializer(serializers.Serializer):
    """
    Serializer for Kactor comparison results.
    """
    dramabeans_id = serializers.UUIDField()
    wiki_id = serializers.UUIDField()
    birthday = serializers.CharField()
    dramabeans_name = serializers.CharField()
    wiki_name = serializers.CharField()
    alternate_names = serializers.ListField()
    best_score = serializers.FloatField()
    wiki_image_url = serializers.CharField()
    dramabeans_image_url = serializers.CharField()
    years_match = serializers.BooleanField()
    is_match = serializers.BooleanField()


# class LinkKactorsSerializer(serializers.Serializer):
#     """Serializer to link Dramabeans Kactor to a Wiki Kactor."""
#     dramabeans_id = serializers.UUIDField()
#     kdrama_id = serializers.UUIDField()


# class UnlinkKactorsSerializer(serializers.Serializer):
#     """Serializer to unlink one or more Dramabeans Kactors."""
#     dramabeans_ids = serializers.ListField(
#         child=serializers.UUIDField(), allow_empty=False
#     )
