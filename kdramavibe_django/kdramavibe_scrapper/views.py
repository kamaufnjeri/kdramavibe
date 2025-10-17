from rest_framework.pagination import PageNumberPagination
from .serializers import KdramaSerializer, KactorSerializer, KactorDetailSerializer, KdramaDetailSerializer
from .models import Kdrama, Kactor
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework import status
import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q

import re


def normalize_name(name: str) -> str:
    if not name:
        return ""

    # Remove spaces, hyphens, underscores, dots, and all Unicode dash variants
    cleaned = re.sub(r"[\s\-\u2010-\u2015._]", "", name)
    return cleaned.lower()


class KdramaFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(method='filter_title', label='Search by title') 
    year = django_filters.CharFilter(method='filter_year', label='Search by year')
    genre = django_filters.CharFilter(method='filter_genres', label='Search by genre')

    class Meta:
        model = Kdrama
        fields = ['title', 'year', 'genre']

    def filter_title(self, queryset, name, value):
        """Search by title or alternate_titles"""
        queryset_matching_title = queryset.filter(Q(title__icontains=value))

        filtered = []
        for kdrama in queryset:
            if any(value.lower() in title.lower() for title in (kdrama.alternate_titles or [])):
                filtered.append(kdrama)

        if filtered:
            return queryset_matching_title | queryset.filter(id__in=[k.id for k in filtered])
        return queryset_matching_title

    def filter_genres(self, queryset, name, value):
        """Filter by genre (list inside JSONField)"""
        filtered = []
        for kdrama in queryset:
            if any(value.lower() in genre.lower() for genre in (kdrama.genres or [])):
                filtered.append(kdrama)
        return queryset.filter(id__in=[k.id for k in filtered])

    def filter_year(self, queryset, name, value):
        """Filter by year range when year is inside start_year and end_year (both strings)"""
        value = str(value).strip()
        return queryset.filter(
            Q(start_year__lte=value) &
            (Q(end_year__gte=value) | Q(end_year__icontains='PRESENT'))
        )



class KactorFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(method='filter_name', label='Search by name') 
    age = django_filters.NumberFilter(field_name='age', lookup_expr='exact', label='Search by age')
    gender = django_filters.CharFilter(method='filter_gender', label='Search by gender')


    class Meta:
        model = Kactor
        fields = ['name', 'age', "gender"]

    def filter_name(self, queryset, name, value):
        """Search by name or alternate_names (normalized for dashes, spaces, etc.)"""
        normalized_value = normalize_name(value)

        filtered = []
        for kactor in queryset:
            # Compare normalized versions of the names
            if normalized_value in normalize_name(kactor.name):
                filtered.append(kactor)
            elif any(
                normalized_value in normalize_name(kactor_name)
                for kactor_name in (kactor.alternate_names or [])
            ):
                filtered.append(kactor)

        if filtered:
            return queryset.filter(id__in=[k.id for k in filtered])
        
        # fallback: search using default contains
        return queryset.filter(Q(name__icontains=value))
    

    def filter_gender(self, queryset, name, value):
        """Normalize and filter by gender."""
        if not value:
            return queryset

        value = value.lower().strip()

        # normalize variations
        if value in ["man", "men", "male", "m"]:
            value_to_use = "male"
        elif value in ["woman", "women", "female", "f"]:
            value_to_use = "female"
        else:
            return queryset

        return queryset.filter(gender__iexact=value_to_use)



class KdramaPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({
            'total_count': self.page.paginator.count,  
            'total_pages': self.page.paginator.num_pages, 
            'current_page': self.page.number, 
            'page_size': self.page_size,  
            'next': self.get_next_link(), 
            'previous': self.get_previous_link(), 
            'results': data
        })


class KdramaListView(ListAPIView):
    queryset = Kdrama.objects.all().order_by('title')
    serializer_class = KdramaSerializer
    pagination_class = KdramaPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = KdramaFilter
    


class KactorListView(ListAPIView):
    queryset = Kactor.objects.all().order_by('name')
    serializer_class =  KactorSerializer
    pagination_class = KdramaPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = KactorFilter

class KdramaDetailView(RetrieveAPIView):
    queryset = Kdrama.objects.all()
    serializer_class = KdramaDetailSerializer
    lookup_field = "slug"


class KactorDetailView(RetrieveAPIView):
    queryset = Kactor.objects.all()
    serializer_class = KactorDetailSerializer
    lookup_field = "slug"

