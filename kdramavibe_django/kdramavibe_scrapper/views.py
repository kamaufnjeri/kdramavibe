"""
Views for Kdrama and Kactor API endpoints, including list, detail, filtering,
pagination, and utility functions for normalization and comparison.
"""

import re
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework import status
import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q

from .serializers import (
    KdramaSerializer,
    KactorSerializer,
    KactorDetailSerializer,
    KdramaDetailSerializer,
    KdramaMatchSerializer,
    LinkKdramasSerializer,
    UnlinkKdramasSerializer,
    KactorMatchSerializer,
)
from .models import Kdrama, Kactor, DramabeansKdrama, DramabeansKactor
from kdramavibe_scrapper.utils import CompareKdramas, CompareKactors


def normalize_name(name: str) -> str:
    """
    Normalize a name by removing spaces, hyphens, underscores, dots, 
    and all Unicode dash variants, then convert to lowercase.
    
    Args:
        name (str): The original name to normalize.
    
    Returns:
        str: Normalized lowercase string.
    """
    if not name:
        return ""

    cleaned = re.sub(r"[\s\-\u2010-\u2015._]", "", name)
    return cleaned.lower()


class KdramaFilter(django_filters.FilterSet):
    """
    FilterSet for Kdrama queryset with title, year, genre, and ordering filters.
    """
    title = django_filters.CharFilter(method='filter_title', label='Search by title')
    year = django_filters.CharFilter(method='filter_year', label='Search by year')
    genre = django_filters.CharFilter(method='filter_genres', label='Search by genre')

    ORDER_CHOICES = [
        ('title_asc', 'Title (A–Z)'),
        ('title_desc', 'Title (Z–A)'),
        ('votes_asc', 'Votes (Ascending)'),
        ('votes_desc', 'Votes (Descending)'),
        ('rating_asc', 'Rating (Ascending)'),
        ('rating_desc', 'Rating (Descending)'),
        ('year_asc', 'Year (Oldest First)'),
        ('year_desc', 'Year (Newest First)'),
    ]

    ordering = django_filters.ChoiceFilter(
        label='Order By',
        choices=ORDER_CHOICES,
        method='filter_ordering'
    )

    class Meta:
        model = Kdrama
        fields = ['title', 'year', 'genre']

    def filter_title(self, queryset, name, value):
        """
        Filter Kdramas by title or any alternate_titles containing the search value.
        """
        queryset_matching_title = queryset.filter(Q(title__icontains=value))

        filtered = [
            kdrama for kdrama in queryset
            if any(value.lower() in title.lower() for title in (kdrama.alternate_titles or []))
        ]

        if filtered:
            return queryset_matching_title | queryset.filter(id__in=[k.id for k in filtered])
        return queryset_matching_title

    def filter_genres(self, queryset, name, value):
        """
        Filter Kdramas by genre, matching against the JSONField genres list.
        """
        filtered = [
            kdrama for kdrama in queryset
            if any(value.lower() in genre.lower() for genre in (kdrama.genres or []))
        ]
        return queryset.filter(id__in=[k.id for k in filtered])

    def filter_year(self, queryset, name, value):
        """
        Filter Kdramas by year, comparing against start_year and end_year.
        Handles ongoing shows with 'PRESENT' in end_year.
        """
        value = str(value).strip()
        return queryset.filter(
            Q(start_year__lte=value) &
            (Q(end_year__gte=value) | Q(end_year__icontains='PRESENT'))
        )

    def filter_ordering(self, queryset, name, value):
        """
        Map user-friendly ordering choices to actual DB fields for ordering.
        """
        order_map = {
            'title_asc': ['title'],
            'title_desc': ['-title'],
            'votes_asc': ['dramabeans_details__no_of_votes'],
            'votes_desc': ['-dramabeans_details__no_of_votes'],
            'rating_asc': ['dramabeans_details__rating'],
            'rating_desc': ['-dramabeans_details__rating'],
            'year_asc': ['start_year', 'end_year'],
            'year_desc': ['-start_year', '-end_year'],
        }

        order_fields = order_map.get(value)
        if order_fields:
            return queryset.order_by(*order_fields)
        return queryset


class KactorFilter(django_filters.FilterSet):
    """
    FilterSet for Kactor queryset with name, age, gender, and ordering filters.
    """
    name = django_filters.CharFilter(method='filter_name', label='Search by name')
    age = django_filters.NumberFilter(field_name='age', lookup_expr='exact', label='Search by age')
    gender = django_filters.CharFilter(method='filter_gender', label='Search by gender')

    ORDER_CHOICES = [
        ('name_asc', 'Name (A–Z)'),
        ('name_desc', 'Name (Z–A)'),
        ('votes_asc', 'Votes (Ascending)'),
        ('votes_desc', 'Votes (Descending)'),
        ('age_asc', 'Age (Ascending)'),
        ('age_desc', 'Age (Descending)'),
    ]

    ordering = django_filters.ChoiceFilter(
        label='Order By',
        choices=ORDER_CHOICES,
        method='filter_ordering'
    )

    class Meta:
        model = Kactor
        fields = ['name', 'age', 'gender']

    def filter_name(self, queryset, name, value):
        """
        Filter Kactors by name or alternate_names, normalizing names for consistent comparison.
        """
        normalized_value = normalize_name(value)

        filtered = [
            kactor for kactor in queryset
            if normalized_value in normalize_name(kactor.name)
            or any(normalized_value in normalize_name(kactor_name)
                   for kactor_name in (kactor.alternate_names or []))
        ]

        if filtered:
            return queryset.filter(id__in=[k.id for k in filtered])

        # fallback to case-insensitive contains
        return queryset.filter(Q(name__icontains=value))

    def filter_gender(self, queryset, name, value):
        """
        Normalize and filter gender values for male/female variations.
        """
        if not value:
            return queryset

        value = value.lower().strip()
        if value in ["man", "men", "male", "m"]:
            value_to_use = "male"
        elif value in ["woman", "women", "female", "f"]:
            value_to_use = "female"
        else:
            return queryset

        return queryset.filter(gender__iexact=value_to_use)

    def filter_ordering(self, queryset, name, value):
        """
        Map user-friendly ordering choices to actual DB fields for Kactor queryset.
        """
        order_map = {
            'name_asc': ['name'],
            'name_desc': ['-name'],
            'votes_asc': ['dramabeans_details__no_of_votes'],
            'votes_desc': ['-dramabeans_details__no_of_votes'],
            'age_asc': ['age'],
            'age_desc': ['-age'],
        }

        order_fields = order_map.get(value)
        if order_fields:
            return queryset.order_by(*order_fields)
        return queryset


class KdramaPagination(PageNumberPagination):
    """
    Custom pagination class for Kdramas and Kactors.
    Includes total_count, total_pages, current_page, page_size, next, previous, results.
    """
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        """
        Return a structured paginated response.
        """
        return Response({
            'total_count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'current_page': self.page.number,
            'page_size': self.page_size,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data,
        })


# List views
class KdramaListView(ListAPIView):
    """API endpoint to list Kdramas with filtering and pagination"""
    queryset = Kdrama.objects.all().order_by('title')
    serializer_class = KdramaSerializer
    pagination_class = KdramaPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = KdramaFilter


class KactorListView(ListAPIView):
    """API endpoint to list Kactors with filtering and pagination"""
    queryset = Kactor.objects.all().order_by('name')
    serializer_class = KactorSerializer
    pagination_class = KdramaPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = KactorFilter


# Detail views
class KdramaDetailView(RetrieveAPIView):
    """API endpoint to retrieve details for a single Kdrama by slug"""
    queryset = Kdrama.objects.all()
    serializer_class = KdramaDetailSerializer
    lookup_field = "slug"


class KactorDetailView(RetrieveAPIView):
    """API endpoint to retrieve details for a single Kactor by slug"""
    queryset = Kactor.objects.all()
    serializer_class = KactorDetailSerializer
    lookup_field = "slug"


# class CompareKdramasView(GenericAPIView):
#     serializer_class = KdramaMatchSerializer
#     pagination_class = KdramaPagination

#     def get_queryset(self):
#         # Base queryset for pagination (Dramabeans side)
#         return DramabeansKdrama.objects.all()


#     def get(self, request, *args, **kwargs):
#         threshold = int(request.query_params.get("threshold", 80))
#         dramabeans_limit = int(request.query_params.get("page_size", 20))  # 👈 limit Wiki set size

#         # Paginate Dramabeans side
#         dramabeans_qs = self.get_queryset()
#         page = self.paginate_queryset(dramabeans_qs)

#         if page is None:
#             return Response(
#                 {"detail": "Pagination failed or no items found."},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         # Load only a subset of Wiki Kdramas
#         wiki_kdramas = Kdrama.objects.all()

#         results = []

#         # Compare only the paginated Dramabeans page against limited Wiki list
#         for dramabeans_kdrama in page:
#             for wiki_item in wiki_kdramas:
#                 cmp = CompareKdramas(dramabeans_kdrama, wiki_item, threshold)
#                 details = cmp.match_details()
#                 if details["is_match"]:
#                     results.append(details)

#         serializer = self.get_serializer(results, many=True)
#         return self.get_paginated_response(serializer.data)

# class LinkKdramasView(GenericAPIView):
#     """
#     POST a list of {dramabeans_id, kdrama_id} pairs to create 1-to-1 relationships.
#     """
#     serializer_class = LinkKdramasSerializer

#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data, many=True)
#         serializer.is_valid(raise_exception=True)

#         linked, errors = [], []

#         for item in serializer.validated_data:
#             d_id = item["dramabeans_id"]
#             k_id = item["kdrama_id"]

#             try:
#                 d = DramabeansKdrama.objects.get(id=d_id)
#                 k = Kdrama.objects.get(id=k_id)

#                 # Protect existing links
#                 if d.kdrama_id and d.kdrama_id != k.id:
#                     errors.append({
#                         "dramabeans_id": d_id,
#                         "error": f"Already linked to Kdrama {d.kdrama_id}"
#                     })
#                     continue

#                 d.kdrama = k
#                 d.save()
#                 linked.append({
#                     "dramabeans_id": d.id,
#                     "dramabeans_title": d.title,
#                     "kdrama_id": k.id,
#                     "kdrama_title": k.title,
#                 })

#             except DramabeansKdrama.DoesNotExist:
#                 errors.append({"dramabeans_id": d_id, "error": "Dramabeans not found"})
#             except Kdrama.DoesNotExist:
#                 errors.append({"kdrama_id": k_id, "error": "Kdrama not found"})

#         return Response({"linked": linked, "errors": errors}, status=status.HTTP_200_OK)


# class UnlinkKdramasView(GenericAPIView):
#     """
#     POST a list of DramabeansKdrama IDs to remove links.
#     """
#     serializer_class = UnlinkKdramasSerializer

#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         dramabeans_ids = serializer.validated_data["dramabeans_ids"]
#         unlinked, errors = [], []

#         for d_id in dramabeans_ids:
#             try:
#                 d = DramabeansKdrama.objects.get(id=d_id)
#                 if d.kdrama_id:
#                     d.kdrama = None
#                     d.save()
#                     unlinked.append({
#                         "dramabeans_id": d.id,
#                         "title": d.title
#                     })
#                 else:
#                     errors.append({"dramabeans_id": d_id, "error": "Already unlinked"})
#             except DramabeansKdrama.DoesNotExist:
#                 errors.append({"dramabeans_id": d_id, "error": "Not found"})

#         return Response({"unlinked": unlinked, "errors": errors}, status=status.HTTP_200_OK)
    
# class CompareKactorsView(GenericAPIView):
#     serializer_class = KactorMatchSerializer
#     pagination_class = KdramaPagination

#     def get_queryset(self):
#         # Base queryset for pagination (Dramabeans side)
#         return DramabeansKactor.objects.all()


#     def get(self, request, *args, **kwargs):
#         threshold = int(request.query_params.get("threshold", 90))
#         dramabeans_limit = int(request.query_params.get("page_size", 20))  # 👈 limit Wiki set size
#         # Paginate Dramabeans side
#         dramabeans_qs = self.get_queryset()
#         print('\n******', dramabeans_qs[0].name)

#         page = self.paginate_queryset(dramabeans_qs)

#         if page is None:
#             return Response(
#                 {"detail": "Pagination failed or no items found."},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         # Load only a subset of Wiki Kdramas
#         wiki_kactors = Kactor.objects.all()

#         results = []

#         # Compare only the paginated Dramabeans page against limited Wiki list
#         for dramabeans_kactor in page:
#             for wiki_item in wiki_kactors:
#                 cmp = CompareKactors(dramabeans_kactor, wiki_item, threshold)
#                 details = cmp.match_details()
#                 if details["is_match"]:
#                     results.append(details)

#         serializer = self.get_serializer(results, many=True)
#         return self.get_paginated_response(serializer.data)
