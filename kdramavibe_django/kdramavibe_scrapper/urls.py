# urls.py
from django.urls import path
from .views import KdramaListView, KactorListView, KdramaDetailView, KactorDetailView

urlpatterns = [
    path('api/kdramas/', KdramaListView.as_view(), name='kdramas-list'),
    path('api/kactors/', KactorListView.as_view(), name='kactors-list'),
    path('api/kdramas/<slug:slug>/', KdramaDetailView.as_view(), name='kdrama-detail'),
    path('api/kactors/<slug:slug>/', KactorDetailView.as_view(), name='kactor-detail'),
]
