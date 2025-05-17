# library/urls.py

from django.urls import path
from .views import (
    GenreListView,
    GenreDetailView,
    GenreCreateView,
    GenreUpdateView,
    GenreDeleteView,
    ComposerListView,
    ComposerDetailView,
    ComposerCreateView,
    ComposerUpdateView,
    ComposerDeleteView,
    ArrangerListView,
    ArrangerDetailView,
    ArrangerCreateView,
    ArrangerUpdateView,
    ArrangerDeleteView,
)

urlpatterns = [
    # Genre URLs
    path("genres/", GenreListView.as_view(), name="genre_list"),
    path("genres/<int:pk>/", GenreDetailView.as_view(), name="genre_detail"),
    path("genres/create/", GenreCreateView.as_view(), name="genre_create"),
    path("genres/<int:pk>/update/", GenreUpdateView.as_view(), name="genre_update"),
    path("genres/<int:pk>/delete/", GenreDeleteView.as_view(), name="genre_delete"),
    # Composer URLs
    path("composers/", ComposerListView.as_view(), name="composer_list"),
    path("composers/<int:pk>/", ComposerDetailView.as_view(), name="composer_detail"),
    path("composers/create/", ComposerCreateView.as_view(), name="composer_create"),
    path(
        "composers/<int:pk>/update/",
        ComposerUpdateView.as_view(),
        name="composer_update",
    ),
    path(
        "composers/<int:pk>/delete/",
        ComposerDeleteView.as_view(),
        name="composer_delete",
    ),
    # Arranger URLs
    path("arrangers/", ArrangerListView.as_view(), name="arranger_list"),
    path("arrangers/<int:pk>/", ArrangerDetailView.as_view(), name="arranger_detail"),
    path("arrangers/create/", ArrangerCreateView.as_view(), name="arranger_create"),
    path(
        "arrangers/<int:pk>/update/",
        ArrangerUpdateView.as_view(),
        name="arranger_update",
    ),
    path(
        "arrangers/<int:pk>/delete/",
        ArrangerDeleteView.as_view(),
        name="arranger_delete",
    ),
]
