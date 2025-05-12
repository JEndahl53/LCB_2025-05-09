# concerts/urls.py
from django.urls import path
from .views import (
    ConductorListView,
    ConductorDetailView,
    ConductorCreateView,
    ConductorUpdateView,
    ConductorDeleteView,
    GuestListView,
    GuestDetailView,
    GuestCreateView,
    GuestUpdateView,
    GuestDeleteView,
)

urlpatterns = [
    path("conductors/", ConductorListView.as_view(), name="conductor_list"),
    path(
        "conductors/<int:pk>/", ConductorDetailView.as_view(), name="conductor_detail"
    ),
    path("conductors/create/", ConductorCreateView.as_view(), name="conductor_create"),
    path(
        "conductors/<int:pk>/update/",
        ConductorUpdateView.as_view(),
        name="conductor_update",
    ),
    path(
        "conductors/<int:pk>/delete/",
        ConductorDeleteView.as_view(),
        name="conductor_delete",
    ),
    path("guests/", GuestListView.as_view(), name="guest_list"),
    path("guests/<int:pk>/", GuestDetailView.as_view(), name="guest_detail"),
    path("guests/create/", GuestCreateView.as_view(), name="guest_create"),
    path("guests/<int:pk>/update/", GuestUpdateView.as_view(), name="guest_update"),
    path("guests/<int:pk>/delete/", GuestDeleteView.as_view(), name="guest_delete"),
]
