# core/forms.py

from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit
from library.models import (
    Composer,
    Arranger,
    Rental_Organization,
    Loaning_Organization,
    Borrowing_Organization,
    Piece,
)
from concerts.models import Conductor, Guest


class PersonBaseForm(forms.ModelForm):
    """Base form for PersonBase models."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Create a form helper (to assist crispy forms)
        self.helper = FormHelper(self)
        self.helper.form_method = "post"
        self.helper.form_tag = False  # Don't render the form tag

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


class OrganizationBaseForm(forms.ModelForm):
    """Base form for OrganizationBase models."""

    class Meta:
        fields = [
            "name",
            "contact_name",
            "contact_email",
            "contact_phone",
            "website",
            "notes",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Apply custom styling to all form fields
        self.helper = FormHelper(self)
        self.helper.form_method = "post"
        self.helper.form_tag = False  # Don't render the form tag

        # Define the explicit field order using Layout
        self.helper.layout = Layout(
            Field("name"),
            Field("contact_name"),
            Field("contact_email"),
            Field("contact_phone"),
            Field("website"),
            Field("notes"),
        )

        # Apply styling to all form fields
        for field_name, field in self.fields.items():
            field.widget.attrs.update(
                {
                    "class": "w-full rounded-md border border-slate-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                }
            )


class RentalOrganizationForm(OrganizationBaseForm):
    class Meta:
        model = Rental_Organization
        fields = OrganizationBaseForm.Meta.fields


class LoaningOrganizationForm(OrganizationBaseForm):
    class Meta:
        model = Loaning_Organization
        fields = OrganizationBaseForm.Meta.fields


class BorrowingOrganizationForm(OrganizationBaseForm):
    class Meta:
        model = Borrowing_Organization
        fields = OrganizationBaseForm.Meta.fields


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
