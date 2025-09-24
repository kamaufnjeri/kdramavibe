# urls.py
from django.urls import path
from .views import KdramaListView, KactorListView

urlpatterns = [
    path('api/kdramas/', KdramaListView.as_view(), name='kdramas-list'),
    path('api/kactors/', KactorListView.as_view(), name='kactors-list'),
]
