# concerts/forms.py
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Venue, Concert


class VenueForm(forms.ModelForm):
    class Meta:
        model = Venue
        fields = "__all__"


class ConcertForm(forms.ModelForm):
    class Meta:
        model = Concert
        fields = "__all__"
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "time": forms.TimeInput(attrs={"type": "time"}),
            "conductor": forms.SelectMultiple(),
            "guests": forms.SelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = "id-ConcertForm"
        self.helper.form_class = "form-horizontal"
        self.helper.form_method = "post"
        self.helper.form_action = "submit_survey"

        self.helper.add_input(Submit("submit", "Submit"))
