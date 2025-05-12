# concerts/views.py
# PersonBase views are in core/views.py
from core.forms import ConductorForm, GuestForm
from library.models import PersonBase
from .models import Conductor, Guest
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
