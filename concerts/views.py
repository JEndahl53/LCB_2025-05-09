# concerts/views.py
# PersonBase views are in core/views.py
from django.views.generic.detail import DetailView

from core.forms import ConductorForm, GuestForm
from library.models import PersonBase
from django.views.generic import (
    DetailView,
    ListView,
    DeleteView,
    UpdateView,
    CreateView,
)
from .models import Conductor, Guest, Venue, Concert
from .forms import VenueForm, ConcertForm
from core.views import (
    PersonBaseDetailView,
    PersonBaseListView,
    PersonBaseCreateView,
    PersonBaseUpdateView,
    PersonBaseDeleteView,
)
from django.urls import reverse_lazy


# Create your views here.
class ConductorListView(PersonBaseListView):
    model = Conductor


class ConductorDetailView(PersonBaseDetailView):
    model = Conductor


class ConductorCreateView(PersonBaseCreateView):
    model = Conductor
    form_class = ConductorForm
    template_name = "people/person_form.html"
    success_url = reverse_lazy("conductor_list")

    def get_model_verbose_name(self):
        return "Conductor"

    def get_model_name_for_url(self):
        return "conductor"


class ConductorUpdateView(PersonBaseUpdateView):
    model = Conductor
    form_class = ConductorForm
    template_name = "people/person_form.html"
    success_url = reverse_lazy("conductor_list")

    def get_model_verbose_name(self):
        return "Conductor"

    def get_model_name_for_url(self):
        return "conductor"


class ConductorDeleteView(PersonBaseDeleteView):
    model = Conductor
    success_url = reverse_lazy("conductor_list")


class GuestListView(PersonBaseListView):
    model = Guest


class GuestDetailView(PersonBaseDetailView):
    model = Guest


class GuestCreateView(PersonBaseCreateView):
    model = Guest
    form_class = GuestForm
    template_name = "people/person_form.html"
    success_url = reverse_lazy("guest_list")

    def get_model_verbose_name(self):
        return "Guest"

    def get_model_name_for_url(self):
        return "guest"


class GuestUpdateView(PersonBaseUpdateView):
    model = Guest
    form_class = GuestForm
    template_name = "people/person_form.html"
    success_url = reverse_lazy("guest_list")

    def get_model_verbose_name(self):
        return "Guest"

    def get_model_name_for_url(self):
        return "guest"


class GuestDeleteView(PersonBaseDeleteView):
    model = Guest
    success_url = reverse_lazy("guest_list")


# Venue Views
class VenueDetailView(DetailView):
    model = Venue
    template_name = "venue/venue_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = VenueForm()
        return context


class VenueListView(ListView):
    model = Venue
    template_name = "venue/venue_list.html"
    context_object_name = "venues"
    paginate_by = 20
    ordering = ["name"]


class VenueCreateView(CreateView):
    model = Venue
    form_class = VenueForm
    template_name = "venue/venue_form.html"
    success_url = reverse_lazy("venue_list")


class VenueUpdateView(UpdateView):
    model = Venue
    form_class = VenueForm
    template_name = "venue/venue_form.html"

    def get_success_url(self):
        return reverse_lazy("venue_detail", kwargs={"pk": self.object.pk})


class VenueDeleteView(DeleteView):
    model = Venue
    template_name = "venue/venue_confirm_delete.html"
    success_url = reverse_lazy("venue_list")


class ConcertListView(ListView):
    model = Concert
    template_name = "concert/concert_list.html"
    context_object_name = "concerts"
    paginate_by = 20
    ordering = ["-date"]


class ConcertDetailView(DetailView):
    model = Concert
    template_name = "concert/concert_detail.html"


class ConcertCreateView(CreateView):
    model = Concert
    form_class = ConcertForm
    template_name = "concert/concert_form.html"
    success_url = reverse_lazy("concert_list")


class ConcertUpdateView(UpdateView):
    model = Concert
    form_class = ConcertForm
    template_name = "concert/concert_form.html"


class ConcertDeleteView(DeleteView):
    model = Concert
    template_name = "concert/concert_confirm_delete.html"
    success_url = reverse_lazy("concert_list")
