# core/forms.py

from django import forms
from library.models import Composer, Arranger
from concerts.models import Conductor, Guest


class PersonBaseForm(forms.ModelForm):
    """Base form for PersonBase models."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Apply custom styling to all form fields
        for field_name, field in self.fields.items():
            field.widget.attrs.update(
                {
                    "class": "w-full rounded-md border border-slate-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                }
            )


class ComposerForm(PersonBaseForm):
    class Meta:
        model = Composer
        fields = "__all__"


class ArrangerForm(PersonBaseForm):
    class Meta:
        model = Arranger
        fields = "__all__"


class ConductorForm(PersonBaseForm):
    class Meta:
        model = Conductor
        fields = "__all__"


class GuestForm(PersonBaseForm):
    class Meta:
        model = Guest
        fields = "__all__"
