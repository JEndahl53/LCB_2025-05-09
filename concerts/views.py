# concerts/views.py
# PersonBase views are in core/views.py

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
    success_url = reverse_lazy("conductor_list")


class ConductorUpdateView(PersonBaseUpdateView):
    model = Conductor
    success_url = reverse_lazy("conductor_list")


class ConductorDeleteView(PersonBaseDeleteView):
    model = Conductor
    success_url = reverse_lazy("conductor_list")


class GuestListView(PersonBaseListView):
    model = Guest


class GuestDetailView(PersonBaseDetailView):
    model = Guest


class GuestCreateView(PersonBaseCreateView):
    model = Guest
    success_url = reverse_lazy("guest_list")


class GuestUpdateView(PersonBaseUpdateView):
    model = Guest
    success_url = reverse_lazy("guest_list")


class GuestDeleteView(PersonBaseDeleteView):
    model = Guest
    success_url = reverse_lazy("guest_list")
