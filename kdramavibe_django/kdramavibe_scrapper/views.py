from rest_framework.pagination import PageNumberPagination
from .serializers import KdramaSerializer, KactorSerializer, KactorDetailSerializer, KdramaDetailSerializer
from .models import Kdrama, Kactor
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework import status
from django.core.management import call_command

class KdramaPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class KdramaListView(ListAPIView):
    queryset = Kdrama.objects.all()
    serializer_class = KdramaSerializer
    pagination_class = KdramaPagination


class KactorListView(ListAPIView):
    queryset = Kactor.objects.all()
    serializer_class = KactorSerializer
    pagination_class = KdramaPagination

class KdramaDetailView(RetrieveAPIView):
    queryset = Kdrama.objects.all()
    serializer_class = KdramaDetailSerializer
    lookup_field = "slug"

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.description or not instance.dramabeans_url:
            serialier = self.get_serializer(instance)
            return Response(serialier.data)
        try:
            call_command(
                "crawl",
                "kdrama_details",
                "-a",
                f"dramabeans_url={instance.dramabeans_url}",
            )
        except Exception as e:
            return Response(
                {"error": f"Scraping failed: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        instance.refresh_from_db()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
class KactorDetailView(RetrieveAPIView):
    queryset = Kactor.objects.all()
    serializer_class = KactorDetailSerializer
    lookup_field = "slug"

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.description or instance.bio or not instance.dramabeans_url:
            serialier = self.get_serializer(instance)
            return Response(serialier.data)
        try:
            call_command(
                "crawl",
                "kactor_details",
                "-a",
                f"dramabeans_url={instance.dramabeans_url}",
            )
        except Exception as e:
            return Response(
                {"error": f"Scraping failed: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        instance.refresh_from_db()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)