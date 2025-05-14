# library/models.py

from django.db import models
from django.urls import reverse


# Create your models here.
class PersonBase(models.Model):
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100)
    instrument = models.CharField(max_length=100, blank=True)

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


class Piece(models.Model):
    # Status choices
    STATUS_OWNED = "OWNED"
    STATUS_RENTED = "RENTED"
    STATUS_ON_LOAN = "ON_LOAN"
    STATUS_BORROWED = "BORROWED"
    STATUS_ARCHIVED = "ARCHIVED"
    STATUS_CHOICES = [
        ("", "----------"),
        (STATUS_OWNED, "Owned"),
        (STATUS_RENTED, "Rented"),
        (STATUS_ON_LOAN, "On Loan"),
        (STATUS_BORROWED, "Borrowed"),
        (STATUS_ARCHIVED, "Archived"),
    ]

    # Difficulty choices
    DIFFICULTY_EASY = "EASY"
    DIFFICULTY_MOD_EASY = "MOD_EASY"
    DIFFICULTY_MODERATE = "MODERATE"
    DIFFICULTY_MOD_DIFFICULT = "MOD_DIFFICULT"
    DIFFICULTY_DIFFICULT = "DIFFICULT"
    DIFFICULTY_CHOICES = [
        ("", "----------"),
        (DIFFICULTY_EASY, "Easy"),
        (DIFFICULTY_MOD_EASY, "Moderately Easy"),
        (DIFFICULTY_MODERATE, "Moderate"),
        (DIFFICULTY_MOD_DIFFICULT, "Moderately Difficult"),
        (DIFFICULTY_DIFFICULT, "Difficult"),
    ]

    title = models.CharField(max_length=200)
    composer = models.ManyToManyField(
        Composer,
    )
    arranger = models.ManyToManyField(
        Arranger,
    )
    genre = models.ManyToManyField(Genre, blank=True)
    publisher = models.ForeignKey(
        Publisher, on_delete=models.SET_NULL, blank=True, null=True
    )
    difficulty = models.CharField(
        max_length=16,
        choices=DIFFICULTY_CHOICES,
        blank=True,
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=STATUS_OWNED,
        blank=True,
    )
    rental_organization = models.ForeignKey(
        RentalOrganization, on_delete=models.SET_NULL, blank=True, null=True
    )
    rental_start_date = models.DateField(blank=True, null=True)
    rental_end_date = models.DateField(blank=True, null=True)
    rental_cost = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    loaning_organization = models.ForeignKey(
        LoaningOrganization, on_delete=models.SET_NULL, blank=True, null=True
    )
    loaning_start_date = models.DateField(blank=True, null=True)
    loaning_end_date = models.DateField(blank=True, null=True)
    borrowing_organization = models.ForeignKey(
        BorrowingOrganization, on_delete=models.SET_NULL, blank=True, null=True
    )
    borrowing_start_date = models.DateField(blank=True, null=True)
    borrowing_end_date = models.DateField(blank=True, null=True)
    copyright_date = models.DateField(blank=True, null=True)
    purchase_date = models.DateField(blank=True, null=True)
    location_drawer = models.CharField(max_length=100, blank=True)
    location_number = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
