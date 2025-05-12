# library/views.py
# PersonBase views are in core/views.py

from library.models import PersonBase
from .models import Composer, Arranger
from core.views import (
    PersonBaseDetailView,
    PersonBaseListView,
    PersonBaseCreateView,
    PersonBaseUpdateView,
    PersonBaseDeleteView,
)
from django.urls import reverse_lazy


# Create your views here.
class ComposerListView(PersonBaseListView):
    model = Composer


class ComposerDetailView(PersonBaseDetailView):
    model = Composer


class ComposerCreateView(PersonBaseCreateView):
    model = Composer
    success_url = reverse_lazy("composer_list")


class ComposerUpdateView(PersonBaseUpdateView):
    model = Composer
    success_url = reverse_lazy("composer_list")


class ComposerDeleteView(PersonBaseDeleteView):
    model = Composer
    success_url = reverse_lazy("composer_list")


class ArrangerListView(PersonBaseListView):
    model = Arranger


class ArrangerDetailView(PersonBaseDetailView):
    model = Arranger


class ArrangerCreateView(PersonBaseCreateView):
    model = Arranger
    success_url = reverse_lazy("arranger_list")


class ArrangerUpdateView(PersonBaseUpdateView):
    model = Arranger
    success_url = reverse_lazy("arranger_list")


class ArrangerDeleteView(PersonBaseDeleteView):
    model = Arranger
    success_url = reverse_lazy("arranger_list")
