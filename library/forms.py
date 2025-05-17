# library/forms.py

from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
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
            "composer": forms.SelectMultiple(),
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
        self.helper.form_action = "submit_survey"

        self.helper.add_input(Submit("submit", "Submit"))
