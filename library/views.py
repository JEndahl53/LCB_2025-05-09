# library/views.py
# PersonBase views are in core/views.py

from core.forms import (
    ComposerForm,
    ArrangerForm,
    RentalOrganizationForm,
    LoaningOrganizationForm,
    BorrowingOrganizationForm,
)
from django.views.generic import (
    CreateView,
    ListView,
    DetailView,
    UpdateView,
    DeleteView,
)
from .models import (
    Composer,
    Arranger,
    Genre,
    Piece,
    Rental_Organization,
    Loaning_Organization,
    Borrowing_Organization,
)
from .forms import GenreForm, PieceForm
from core.views import (
    PersonBaseDetailView,
    PersonBaseListView,
    PersonBaseCreateView,
    PersonBaseUpdateView,
    PersonBaseDeleteView,
    OrganizationBaseDetailView,
    OrganizationBaseListView,
    OrganizationBaseCreateView,
    OrganizationBaseUpdateView,
    OrganizationBaseDeleteView,
)
from django.urls import reverse_lazy


# Create your views here.
class ComposerListView(PersonBaseListView):
    model = Composer


class ComposerDetailView(PersonBaseDetailView):
    model = Composer


class ComposerCreateView(PersonBaseCreateView):
    model = Composer
    class_form = ComposerForm
    template_name = "people/person_form.html"
    success_url = reverse_lazy("composer_list")

    def get_model_verbose_name(self):
        return "Composer"

    def get_model_name_for_url(self):
        return "composer"


class ComposerUpdateView(PersonBaseUpdateView):
    model = Composer
    class_form = ComposerForm
    template_name = "people/person_form.html"
    success_url = reverse_lazy("composer_list")

    def get_model_verbose_name(self):
        return "Composer"

    def get_model_name_for_url(self):
        return "composer"


class ComposerDeleteView(PersonBaseDeleteView):
    model = Composer
    success_url = reverse_lazy("composer_list")


class ArrangerListView(PersonBaseListView):
    model = Arranger


class ArrangerDetailView(PersonBaseDetailView):
    model = Arranger


class ArrangerCreateView(PersonBaseCreateView):
    model = Arranger
    class_form = ArrangerForm
    template_name = "people/person_form.html"
    success_url = reverse_lazy("arranger_list")

    def get_model_verbose_name(self):
        return "Arranger"

    def get_model_name_for_url(self):
        return "arranger"


class ArrangerUpdateView(PersonBaseUpdateView):
    model = Arranger
    class_form = ArrangerForm
    template_name = "people/person_form.html"
    success_url = reverse_lazy("arranger_list")

    def get_model_verbose_name(self):
        return "Arranger"

    def get_model_name_for_url(self):
        return "arranger"


class ArrangerDeleteView(PersonBaseDeleteView):
    model = Arranger
    success_url = reverse_lazy("arranger_list")


class GenreListView(ListView):
    model = Genre
    template_name = "genre/genre_list.html"
    context_object_name = "genres"


class GenreDetailView(DetailView):
    model = Genre
    template_name = "genre/genre_detail.html"


class GenreCreateView(CreateView):
    model = Genre
    form_class = GenreForm
    template_name = "genre/genre_form.html"
    success_url = reverse_lazy("genre_list")


class GenreUpdateView(UpdateView):
    model = Genre
    form_class = GenreForm
    template_name = "genre/genre_form.html"


class GenreDeleteView(DeleteView):
    model = Genre
    template_name = "genre/genre_confirm_delete.html"
    success_url = reverse_lazy("genre_list")


class PieceListView(ListView):
    model = Piece
    template_name = "piece/piece_list.html"
    context_object_name = "pieces"


class PieceDetailView(DetailView):
    model = Piece
    template_name = "piece/piece_detail.html"


class PieceCreateView(CreateView):
    model = Piece
    form_class = PieceForm
    template_name = "piece/piece_form.html"
    success_url = reverse_lazy("piece_list")


class PieceUpdateView(UpdateView):
    model = Piece
    form_class = PieceForm
    template_name = "piece/piece_form.html"


class PieceDeleteView(DeleteView):
    model = Piece
    template_name = "piece/piece_confirm_delete.html"
    success_url = reverse_lazy("piece_list")


# Rental Organization views
class RentalOrganizationListView(OrganizationBaseListView):
    model = Rental_Organization


class RentalOrganizationDetailView(OrganizationBaseDetailView):
    model = Rental_Organization


class RentalOrganizationCreateView(OrganizationBaseCreateView):
    model = Rental_Organization
    class_form = RentalOrganizationForm
    template_name = "organizations/organization_form.html"
    success_url = reverse_lazy("rental_organization_list")

    def get_model_verbose_name(self):
        return "Rental Organization"

    def get_model_name_for_url(self):
        return "rental_organization"


class RentalOrganizationUpdateView(OrganizationBaseUpdateView):
    model = Rental_Organization
    class_form = RentalOrganizationForm
    template_name = "organizations/organization_form.html"
    success_url = reverse_lazy("rental_organization_list")

    def get_model_verbose_name(self):
        return "Rental Organization"

    def get_model_name_for_url(self):
        return "rental_organization"


class RentalOrganizationDeleteView(OrganizationBaseDeleteView):
    model = Rental_Organization
    success_url = reverse_lazy("rental_organization_list")


# Loaning Organization views
class LoaningOrganizationListView(OrganizationBaseListView):
    model = Loaning_Organization


class LoaningOrganizationDetailView(OrganizationBaseDetailView):
    model = Loaning_Organization
    template_name = "organizations/organization_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["organization"] = self.object
        context["get_model_verbose_name_plural"] = "Loaning Organizations"
        context["get_model_verbose_name"] = "Loaning Organization"

        return context


class LoaningOrganizationCreateView(OrganizationBaseCreateView):
    model = Loaning_Organization
    class_form = LoaningOrganizationForm
    template_name = "organizations/organization_form.html"
    success_url = reverse_lazy("loaning_organization_list")

    def get_model_verbose_name(self):
        return "Loaning Organization"

    def get_model_name_for_url(self):
        return "loaning_organization"


class LoaningOrganizationUpdateView(OrganizationBaseUpdateView):
    model = Loaning_Organization
    class_form = LoaningOrganizationForm
    template_name = "organizations/organization_form.html"
    success_url = reverse_lazy("loaning_organization_list")

    def get_model_verbose_name(self):
        return "Loaning Organization"

    def get_model_name_for_url(self):
        return "loaning_organization"


class LoaningOrganizationDeleteView(OrganizationBaseDeleteView):
    model = Loaning_Organization
    success_url = reverse_lazy("loaning_organization_list")

    def get_model_verbose_name_plural(self):
        return "Loaning Organizations"


# Borrowing Organization views
class BorrowingOrganizationListView(OrganizationBaseListView):
    model = Borrowing_Organization


class BorrowingOrganizationDetailView(OrganizationBaseDetailView):
    model = Borrowing_Organization


class BorrowingOrganizationCreateView(OrganizationBaseCreateView):
    model = Borrowing_Organization
    class_form = BorrowingOrganizationForm
    template_name = "organizations/organization_form.html"
    success_url = reverse_lazy("borrowing_organization_list")

    def get_model_verbose_name(self):
        return "Borrowing Organization"

    def get_model_name_for_url(self):
        return "borrowing_organization"


class BorrowingOrganizationUpdateView(OrganizationBaseUpdateView):
    model = Borrowing_Organization
    class_form = BorrowingOrganizationForm
    template_name = "organizations/organization_form.html"
    success_url = reverse_lazy("borrowing_organization_list")

    def get_model_verbose_name(self):
        return "Borrowing Organization"

    def get_model_name_for_url(self):
        return "borrowing_organization"


class BorrowingOrganizationDeleteView(OrganizationBaseDeleteView):
    model = Borrowing_Organization
    success_url = reverse_lazy("borrowing_organization_list")
