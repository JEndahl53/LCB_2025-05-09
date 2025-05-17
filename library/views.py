# library/views.py
# PersonBase views are in core/views.py

from core.forms import ComposerForm, ArrangerForm
from django.views.generic import (
    CreateView,
    ListView,
    DetailView,
    UpdateView,
    DeleteView,
)
from .models import Composer, Arranger, Genre, Piece
from .forms import GenreForm, PieceForm
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
