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


class PersonBaseListView(ListView):
    template_name = "people/person_list.html"  # generic template
    context_object_name = "people"
    paginate_by = 20

    def get_model_name_for_url(self):
        return self.model.__name__.lower()

    def get_model_verbose_name_plural(self):
        return self.model._meta.verbose_name_plural

    # Must specify a model in subclasses


class PersonBaseDetailView(DetailView):
    template_name = "people/person_detail.html"  # generic template
    context_object_name = "person"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get the model name for URL construction (e.g.'conductor', 'guest')
        model_name = self.model._meta.model_name.lower()
        context["model_name_for_url"] = model_name
        return context


class PersonBaseCreateView(CreateView):
    template_name = "people/person_form.html"  # generic template
    success_url = reverse_lazy("person_list")  # where to go after successful creation

    def get_form_class(self):  # go after successful creation
        """Return the form class to use in this view."""
        if hasattr(self, "form_class") and self.form_class is not None:
            return self.form_class
        else:
            # Default to all fields if no form_class is specified
            from django.forms import modelform_factory

            return modelform_factory(self.model, fields="__all__")

    def get_model_verbose_name(self):
        """Return the verbose name of the model."""
        return self.model._meta.verbose_name


class PersonBaseUpdateView(UpdateView):
    template_name = "people/person_form.html"  # generic template
    success_url = reverse_lazy("person_list")

    def get_form_class(self):
        """Return the form class to use in this view."""
        if hasattr(self, "form_class") and self.form_class is not None:
            return self.form_class
        else:
            # Default to all fields if no form_class is specified
            from django.forms import modelform_factory

            return modelform_factory(self.model, fields="__all__")

    def get_model_verbose_name(self):
        """Return the verbose name of the model."""
        return self.model._meta.verbose_name


class PersonBaseDeleteView(DeleteView):
    template_name = "people/person_confirm_delete.html"  # generic template
    success_url = reverse_lazy("person_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get the model name for URL construction (e.g.'conductor', 'guest')
        context["model_name_for_url"] = self.model.__name__.lower()
        context["person"] = self.get_object()
        return context

    def get_model_name_for_url(self):
        return self.model.__name__.lower()
