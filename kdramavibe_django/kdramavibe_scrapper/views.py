from rest_framework.pagination import PageNumberPagination
from .serializers import KdramaSerializer, KactorSerializer
from .models import Kdrama, Kactor
from rest_framework.generics import ListAPIView

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