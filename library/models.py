# library/models.py
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse


# Create your models here.
class PersonBase(models.Model):
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.last_name}, {self.first_name}"

    def get_sort_name(self):
        return f"{self.last_name}, {self.first_name}"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_absolute_url(self):
        raise NotImplementedError("Subclasses must implement get_absolute_url().")

    class Meta:
        ordering = ["last_name", "first_name"]
        abstract = True


class Composer(PersonBase):
    birth_year = models.IntegerField(blank=True, null=True)

    def get_absolute_url(self):
        return reverse("composer_detail", args=[str(self.id)])

    class Meta:
        verbose_name = "Composer"
        verbose_name_plural = "Composers"


class Arranger(PersonBase):
    pass

    def get_absolute_url(self):
        return reverse("arranger_detail", args=[str(self.id)])

    class Meta:
        verbose_name = "Arranger"
        verbose_name_plural = "Arrangers"


class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("genre_detail", args=[str(self.id)])

    class Meta:
        verbose_name = "Genre"
        verbose_name_plural = "Genres"
        ordering = ["name"]


class Publisher(models.Model):
    name = models.CharField(max_length=100)
    website = models.URLField(blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("publisher_detail", args=[str(self.id)])

    class Meta:
        verbose_name_plural = "publishers"
        ordering = ["name"]


class Organization(models.Model):
    name = models.CharField(max_length=100)
    contact_name = models.CharField(max_length=100)
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        raise NotImplementedError("Subclasses must implement get_absolute_url().")

    class Meta:
        ordering = ["name"]
        abstract = True


class RentalOrganization(Organization):
    pass

    def get_absolute_url(self):
        return reverse("rental_organization_detail", args=[str(self.id)])


class LoaningOrganization(Organization):
    pass

    def get_absolute_url(self):
        return reverse("loaning_organization_detail", args=[str(self.id)])


class BorrowingOrganization(Organization):
    pass

    def get_absolute_url(self):
        return reverse("borrowing_organization_detail", args=[str(self.id)])


class PieceStatus(models.TextChoices):
    NONE = "", "---------"
    OWNED = "OWNED", "Owned"
    RENTED = "RENTED", "Rented"
    ON_LOAN = "ON_LOAN", "On Loan"
    BORROWED = "BORROWED", "Borrowed"
    ARCHIVED = "ARCHIVED", "Archived"


class PieceDifficulty(models.TextChoices):
    NONE = "", "---------"
    EASY = "EASY", "Easy"
    MOD_EASY = "MOD_EASY", "Moderately Easy"
    MODERATE = "MODERATE", "Moderate"
    MOD_DIFFICULT = "MOD_DIFFICULT", "Moderately Difficult"
    DIFFICULT = "DIFFICULT", "Difficult"


class Piece(models.Model):
    # Basic information
    title = models.CharField(max_length=200)
    composer = models.ManyToManyField(Composer, blank=True)
    arranger = models.ManyToManyField(Arranger, blank=True)
    genre = models.ManyToManyField(Genre, blank=True)
    publisher = models.ForeignKey(
        Publisher, on_delete=models.SET_NULL, blank=True, null=True
    )
    difficulty = models.CharField(
        max_length=16, choices=PieceDifficulty.choices, blank=True, default=""
    )

    # Status and location
    status = models.CharField(
        max_length=10,
        choices=PieceStatus.choices,
        default=PieceStatus.NONE,
        blank=True,
    )
    location_drawer = models.CharField(max_length=100, blank=True)
    location_number = models.CharField(max_length=100, blank=True)

    # Rental info
    rental_organization = models.ForeignKey(
        RentalOrganization, on_delete=models.SET_NULL, blank=True, null=True
    )
    rental_start_date = models.DateField(blank=True, null=True)
    rental_end_date = models.DateField(blank=True, null=True)
    rental_cost = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )

    # Loaned to info
    loaning_organization = models.ForeignKey(
        LoaningOrganization, on_delete=models.SET_NULL, blank=True, null=True
    )
    loaning_start_date = models.DateField(blank=True, null=True)
    loaning_end_date = models.DateField(blank=True, null=True)

    # Borrowed from info
    borrowing_organization = models.ForeignKey(
        BorrowingOrganization, on_delete=models.SET_NULL, blank=True, null=True
    )
    borrowing_start_date = models.DateField(blank=True, null=True)
    borrowing_end_date = models.DateField(blank=True, null=True)

    # Miscellaneous info
    copyright_date = models.DateField(blank=True, null=True)
    purchase_date = models.DateField(blank=True, null=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_composers_display(self):
        return "; ".join(str(composer) for composer in self.composer.all())

    def get_arrangers_display(self):
        return "; ".join(str(arranger) for arranger in self.arranger.all())

    def get_genres_display(self):
        return "; ".join(str(genre) for genre in self.genre.all())

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("piece_detail", args=[str(self.id)])

    def clean(self):
        errors = {}

        # could add date checks as well, but that may be overkill
        if self.status == PieceStatus.RENTED and not self.rental_organization:
            errors["rental_organization"] = (
                "Rental organization is required for rented pieces."
            )
        if self.status == PieceStatus.ON_LOAN and not self.loaning_organization:
            errors["loaning_organization"] = (
                "Loaning organization is required for on loan pieces."
            )
        if self.status == PieceStatus.BORROWED and not self.borrowing_organization:
            errors["borrowing_organization"] = (
                "Borrowing organization is required for borrowed pieces."
            )
        if errors:
            raise ValidationError(errors)

    class Meta:
        ordering = ["title"]
        indexes = [
            models.Index(fields=["title"]),
        ]
