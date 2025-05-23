# library/forms.py

from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout
from .models import Genre, Piece


class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = "__all__"


class PieceForm(forms.ModelForm):
    class Meta:
        model = Piece
        fields = "__all__"
        widgets = {
            "composer": forms.SelectMultiple(
                attrs={"class": "hidden"}
            ),  # Hide but keep it for form submission
            "arranger": forms.SelectMultiple(),
            "genre": forms.SelectMultiple(),
            "difficulty": forms.Select(),
            "status": forms.Select(),
            "purchase_date": forms.SelectDateWidget(),
            "rental_organization": forms.Select(),
            "rental_start_date": forms.SelectDateWidget(),
            "rental_end_date": forms.SelectDateWidget(),
            "borrowing_organization": forms.Select(),
            "borrowing_start_date": forms.SelectDateWidget(),
            "borrowing_end_date": forms.SelectDateWidget(),
            "loaning_organization": forms.Select(),
            "loaning_start_date": forms.SelectDateWidget(),
            "loaning_end_date": forms.SelectDateWidget(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = "id-PieceForm"
        self.helper.form_class = "form-horizontal"
        self.helper.form_method = "post"

        # Exclude composer field from the form layout
        self.fields["composer"].label = ""  # Remove label

        # Create a layout that excludes the composer field from normal rendering
        # This defines which fields show up in the {{ form|crispy }} rendering
        visible_fields = [field for field in self.fields if field != "composer"]

        # Add the fields explicitly to control their rendering order and grouping
        self.helper.layout = Layout(
            # All fields except composer - they'll be rendered by the crispy filter in the template
        )
