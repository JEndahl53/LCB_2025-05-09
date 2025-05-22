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
    RentalOrganizationListView,
    RentalOrganizationDetailView,
    RentalOrganizationCreateView,
    RentalOrganizationUpdateView,
    RentalOrganizationDeleteView,
    LoaningOrganizationListView,
    LoaningOrganizationDetailView,
    LoaningOrganizationCreateView,
    LoaningOrganizationUpdateView,
    LoaningOrganizationDeleteView,
    BorrowingOrganizationListView,
    BorrowingOrganizationDetailView,
    BorrowingOrganizationCreateView,
    BorrowingOrganizationUpdateView,
    BorrowingOrganizationDeleteView,
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
    # Rental Organizations URLs
    path(
        "rental_organizations/",
        RentalOrganizationListView.as_view(),
        name="rental_organization_list",
    ),
    path(
        "rental_organizations/<int:pk>/",
        RentalOrganizationDetailView.as_view(),
        name="rental_organization_detail",
    ),
    path(
        "rental_organizations/create/",
        RentalOrganizationCreateView.as_view(),
        name="rental_organization_create",
    ),
    path(
        "rental_organizations/<int:pk>/update/",
        RentalOrganizationUpdateView.as_view(),
        name="rental_organization_update",
    ),
    path(
        "rental_organizations/<int:pk>/delete/",
        RentalOrganizationDeleteView.as_view(),
        name="rental_organization_delete",
    ),
    # Loaning Organizations URLs
    path(
        "loaning_organizations/",
        LoaningOrganizationListView.as_view(),
        name="loaning_organization_list",
    ),
    path(
        "loaning_organizations/<int:pk>/",
        LoaningOrganizationDetailView.as_view(),
        name="loaning_organization_detail",
    ),
    path(
        "loaning_organizations/create/",
        LoaningOrganizationCreateView.as_view(),
        name="loaning_organization_create",
    ),
    path(
        "loaning_organizations/<int:pk>/update/",
        LoaningOrganizationUpdateView.as_view(),
        name="loaning_organization_update",
    ),
    path(
        "loaning_organizations/<int:pk>/delete/",
        LoaningOrganizationDeleteView.as_view(),
        name="loaning_organization_delete",
    ),
    # Borrowing Organizations URLs
    path(
        "borrowing_organizations/",
        BorrowingOrganizationListView.as_view(),
        name="borrowing_organization_list",
    ),
    path(
        "borrowing_organizations/<int:pk>/",
        BorrowingOrganizationDetailView.as_view(),
        name="borrowing_organization_detail",
    ),
    path(
        "borrowing_organizations/create/",
        BorrowingOrganizationCreateView.as_view(),
        name="borrowing_organization_create",
    ),
    path(
        "borrowing_organizations/<int:pk>/update/",
        BorrowingOrganizationUpdateView.as_view(),
        name="borrowing_organization_update",
    ),
    path(
        "borrowing_organizations/<int:pk>/delete/",
        BorrowingOrganizationDeleteView.as_view(),
        name="borrowing_organization_delete",
    ),
]
