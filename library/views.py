# library/views.py
# PersonBase views are in core/views.py

from core.forms import (
    ComposerForm,
    ArrangerForm,
    RentalOrganizationForm,
    LoaningOrganizationForm,
    BorrowingOrganizationForm,
    PieceForm,
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

# More for HTMX
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST, require_GET
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.contrib.auth.decorators import login_required
import json


# HTMX view for searching composers
def parse_selected_ids(request, method="POST"):
    """
    Helper function to parse selected IDs from the request.
    Handles both POST and GET requests.
    """
    if method == "POST":
        selected_ids = request.POST.getlist("selected_ids", [])
        fallback = request.POST.get("selected_ids")
    else:  # GET
        selected_ids = request.GET.getlist("selected_ids", [])
        fallback = request.GET.get("selected_ids")

    # If we received a non-list format (happens with single values)
    if not selected_ids and fallback:
        try:
            # Try to parse as JSON
            selected_ids = json.loads(fallback)
        except json.JSONDecodeError:
            # If it's not valid JSON, treat as a comma-separated string
            selected_ids = [
                id.strip("\"'") for id in fallback.strip("[]").split(",") if id.strip()
            ]

    # Make sure we're working with strings
    return [str(id).strip("\"'") for id in selected_ids if id]


@require_POST
def search_composer(request):
    query = request.POST.get("composer_search", "").strip()
    selected_ids = parse_selected_ids(request)

    if not query:
        composers = Composer.objects.all().order_by("last_name", "first_name")[:20]
    else:
        composers = Composer.objects.filter(
            Q(last_name__icontains=query) | Q(first_name__icontains=query)
        ).order_by("last_name", "first_name")[:20]

        # Filter out already selected composers
        if selected_ids:
            composers = composers.exclude(id__in=selected_ids)

    html = render_to_string(
        "htmx/_composer_search_results.html",
        {
            "composers": composers,
            "selected_ids": selected_ids,
        },
    )
    return HttpResponse(html)


# HTMX view for adding a composer to the selection
@require_POST
def add_composer(request):
    composer_id = str(request.POST.get("composer_id"))
    composer = get_object_or_404(Composer, id=composer_id)

    # Get currently selected composers
    selected_ids = parse_selected_ids(request)

    # Add the new composer ID if it's not already in the list
    if composer_id not in selected_ids:
        selected_ids.append(composer_id)

    # Get all selected composers by ID
    selected_composers = Composer.objects.filter(id__in=selected_ids)

    # Get search query if provided (for refreshing search results)
    query = request.POST.get("composer_search", "").strip()

    # Prepare search results (composers not already selected)
    if not query:
        search_composers = Composer.objects.exclude(id__in=selected_ids).order_by(
            "last_name", "first_name"
        )[:20]
    else:
        search_composers = (
            Composer.objects.filter(
                Q(last_name__icontains=query) | Q(first_name__icontains=query)
            )
            .exclude(id__in=selected_ids)
            .order_by("last_name", "first_name")[:20]
        )

    # Update the selected composers area
    selected_html = render_to_string(
        "htmx/_selected_composers.html",
        {"composers": selected_composers, "selected_ids": selected_ids},
    )

    # Render the search results
    search_html = render_to_string(
        "htmx/_composer_search_results.html",
        {"composers": search_composers, "selected_ids": selected_ids},
    )

    # Add a script to update both areas
    response_html = f"""
    <div id="selected-composers-update" style="display: none;">{selected_html}</div>
    <div id="search-results-update" style="display: none;">{search_html}</div>
    <script>
        document.getElementById("selected-composers").innerHTML = 
            document.getElementById("selected-composers-update").innerHTML;
        document.getElementById("composer-results").innerHTML =
            document.getElementById("search-results-update").innerHTML;
        document.getElementById("selected-composers-update").remove();
        document.getElementById("search-results-update").remove();
    </script>
    """

    return HttpResponse(response_html)


# HTMX view for removing a composer from the selection
@require_POST
def remove_composer(request):
    composer_id = request.POST.get("composer_id")

    # Get currently selected composers
    selected_ids = parse_selected_ids(request)

    # Remove the composer ID from the list
    if composer_id in selected_ids:
        selected_ids.remove(composer_id)

    # Get all selected composers by ID
    selected_composers = Composer.objects.filter(id__in=selected_ids)

    # Get search query if provided (for refreshing search results)
    query = request.POST.get("composer_search", "").strip()

    # Prepare search results (composers not already selected)
    if not query:
        search_composers = Composer.objects.exclude(id__in=selected_ids).order_by(
            "last_name", "first_name"
        )[:20]
    else:
        search_composers = (
            Composer.objects.filter(
                Q(last_name__icontains=query) | Q(first_name__icontains=query)
            )
            .exclude(id__in=selected_ids)
            .order_by("last_name", "first_name")[:20]
        )

    # Update the selected composers area
    selected_html = render_to_string(
        "htmx/_selected_composers.html",
        {"composers": selected_composers, "selected_ids": selected_ids},
    )

    # Render the search results
    search_html = render_to_string(
        "htmx/_composer_search_results.html",
        {"composers": search_composers, "selected_ids": selected_ids},
    )

    # Create response with both updated areas
    response_html = f"""
    <div id="selected-composers-update" style="display: none;">{selected_html}</div>
    <div id="search-results-update" style="display: none;">{search_html}</div>
    <script>
        document.getElementById("selected-composers").innerHTML = 
            document.getElementById("selected-composers-update").innerHTML;
        document.getElementById("composer-results").innerHTML =
            document.getElementById("search-results-update").innerHTML;
        document.getElementById("selected-composers-update").remove();
        document.getElementById("search-results-update").remove();
    </script>
    """

    return HttpResponse(response_html)


@require_GET
def composer_create_modal(request):
    """
    Returns the HTML for the composer creation modal dialog.
    This gets loaded via HTMX when the "New Composer" button is clicked.
    """
    form = ComposerForm()

    # Get currently selected composers
    selected_ids = parse_selected_ids(request, method="GET")

    html = render_to_string(
        "htmx/_composer_create_modal.html", {"form": form, "selected_ids": selected_ids}
    )
    return HttpResponse(html)


@require_POST
def save_new_composer(request):
    """
    Handles the form submission for creating a new composer.
    If successful, adds the new composer to the selected composer list.
    """
    form = ComposerForm(request.POST)

    # Get currently selected composers
    selected_ids = parse_selected_ids(request)

    if form.is_valid():
        # Save the new composer
        composer = form.save()

        # Add the new composer to the selected list
        selected_ids.append(str(composer.id))

        # Get all selected composers
        selected_composers = Composer.objects.filter(id__in=selected_ids)

        # Render the updated selected composers area
        selected_html = render_to_string(
            "htmx/_selected_composers.html",
            {"composers": selected_composers, "selected_ids": selected_ids},
        )

        # Get updated search results (composers not already selected)
        search_composers = Composer.objects.exclude(id__in=selected_ids).order_by(
            "last_name", "first_name"
        )[:20]

        # Render the search results
        search_html = render_to_string(
            "htmx/_composer_search_results.html",
            {"composers": search_composers, "selected_ids": selected_ids},
        )

        # Create response that updates both areas and closes the modal
        response_html = f"""
        <div id="selected-composers-update" style="display: none;">{selected_html}</div>
        <div id="search-results-update" style="display: none;">{search_html}</div>
        <script>
            document.getElementById("selected-composers").innerHTML = 
                document.getElementById("selected-composers-update").innerHTML;
            document.getElementById("composer-results").innerHTML =
                document.getElementById("search-results-update").innerHTML;
            document.getElementById("modal-container").classList.add("hidden");
            document.getElementById("selected-composers-update").remove();
            document.getElementById("search-results-update").remove();
        </script>
        """

        return HttpResponse(response_html)
    else:
        # If the form is not valid, return the form with errors
        html = render_to_string(
            "htmx/_composer_create_modal.html",
            {"form": form, "selected_ids": selected_ids},
        )
        return HttpResponse(html)


# Create your views here.
class ComposerListView(PersonBaseListView):
    model = Composer


class ComposerDetailView(PersonBaseDetailView):
    model = Composer


class ComposerCreateView(PersonBaseCreateView):
    model = Composer
    form_class = ComposerForm
    template_name = "people/person_form.html"
    success_url = reverse_lazy("composer_list")

    def get_model_verbose_name(self):
        return "Composer"

    def get_model_name_for_url(self):
        return "composer"


class ComposerUpdateView(PersonBaseUpdateView):
    model = Composer
    form_class = ComposerForm
    template_name = "people/person_form.html"

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
    form_class = ArrangerForm
    template_name = "people/person_form.html"
    success_url = reverse_lazy("arranger_list")

    def get_model_verbose_name(self):
        return "Arranger"

    def get_model_name_for_url(self):
        return "arranger"


class ArrangerUpdateView(PersonBaseUpdateView):
    model = Arranger
    form_class = ArrangerForm
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["all_composers"] = Composer.objects.all().order_by(
            "last_name", "first_name"
        )[:20]
        return context


class PieceUpdateView(UpdateView):
    model = Piece
    form_class = PieceForm
    template_name = "piece/piece_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["all_composers"] = Composer.objects.all().order_by(
            "last_name", "first_name"
        )[:20]
        return context


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
