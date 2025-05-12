# core/views.py
# This file is for shared base class views.

from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.urls import reverse_lazy


def get_model_verbose_name_plural(self):
    return self._meta.verbose_name_plural


class PersonBaseListView(ListView):
    template_name = "people/person_list.html"  # generic template
    context_object_name = "people"
    paginate_by = 20

    # Must specify a model in subclasses


class PersonBaseDetailView(DetailView):
    template_name = "people/person_detail.html"  # generic template
    context_object_name = "person"


class PersonBaseCreateView(CreateView):
    template_name = "people/person_form.html"  # generic template
    fields = "__all__"  # all fields in model
    success_url = reverse_lazy("person_list")  # where to go after successful creation


class PersonBaseUpdateView(UpdateView):
    template_name = "people/person_form.html"  # generic template
    fields = "__all__"  # all fields in model


class PersonBaseDeleteView(DeleteView):
    template_name = "people/person_confirm_delete.html"  # generic template
    success_url = reverse_lazy("person_list")
