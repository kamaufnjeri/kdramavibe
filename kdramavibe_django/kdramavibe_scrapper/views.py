from rest_framework.pagination import PageNumberPagination
from .serializers import KdramaSerializer, KactorSerializer, KactorDetailSerializer, KdramaDetailSerializer
from .models import Kdrama, Kactor
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework import status
import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q


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
    occupation = django_filters.CharFilter(method='filter_occupations', label='Search by occupation')
    age = django_filters.NumberFilter(field_name='age', lookup_expr='exact', label='Search by age')


    class Meta:
        model = Kactor
        fields = ['name', 'occupation', 'age']

    def filter_name(self, queryset, name, value):
        """Search by title or alternate_titles"""
        queryset_matching_name = queryset.filter(Q(name__icontains=value))

        filtered = []
        for kactor in queryset:
            if any(value.lower() in kactor_name.lower() for kactor_name in (kactor.alternate_names or [])):
                filtered.append(kactor)

        if filtered:
            return queryset_matching_name | queryset.filter(id__in=[k.id for k in filtered])
        return queryset_matching_name

    def filter_occupations(self, queryset, name, value):
        """Filter by genre (list inside JSONField)"""
        filtered = []
        for kactor in queryset:
            if any(value.lower() in occupation.lower() for occupation in (kactor.occupations or [])):
                filtered.append(kactor)
        return queryset.filter(id__in=[k.id for k in filtered])

    


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

