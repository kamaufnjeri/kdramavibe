"""
URL patterns for Kdrama and Kactor API endpoints, including list, detail,
compare, link, and unlink operations.
"""

from django.urls import path
from .views import (
    KdramaListView,
    KactorListView,
    KdramaDetailView,
    KactorDetailView,
    # CompareKdramasView,
    # LinkKdramasView,
    # UnlinkKdramasView,
    # CompareKactorsView,
)

urlpatterns = [
    # Kdrama API endpoints
    path(
        "api/kdramas/",
        KdramaListView.as_view(),
        name="kdramas-list",
    ),
    path(
        "api/kactors/",
        KactorListView.as_view(),
        name="kactors-list",
    ),
    path(
        "api/kdramas/<slug:slug>/",
        KdramaDetailView.as_view(),
        name="kdrama-detail",
    ),
    path(
        "api/kactors/<slug:slug>/",
        KactorDetailView.as_view(),
        name="kactor-detail",
    ),

    # Compare and link/unlink Kdramas
    # path(
    #     "api/kdramas/compare/",
    #     CompareKdramasView.as_view(),
    #     name="compare-kdramas",
    # ),
    # path(
    #     "api/kdramas/link/",
    #     LinkKdramasView.as_view(),
    #     name="link-kdramas",
    # ),
    # path(
    #     "api/kdramas/unlink/",
    #     UnlinkKdramasView.as_view(),
    #     name="unlink-kdramas",
    # ),

    # # Compare Kactors
    # path(
    #     "api/kactors/compare/",
    #     CompareKactorsView.as_view(),
    #     name="compare-kactors",
    # ),
]
