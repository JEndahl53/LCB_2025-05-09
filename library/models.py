# library/models.py
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


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
        ordering = ["last_name", "first_name"]
        verbose_name = "Composer"
        verbose_name_plural = "Composers"


class Arranger(PersonBase):

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


# New link between Organization and Piece
class PieceOrganizationRelationship(models.Model):
    """Manages the relationship between organizations and pieces."""

    # Relationship type constants
    RENTED = "RENTED"
    ON_LOAN = "ON_LOAN"
    BORROWED = "BORROWED"

    RELATIONSHIP_TYPES = [
        (RENTED, "Rented"),
        (ON_LOAN, "On Loan"),
        (BORROWED, "Borrowed"),
    ]
    piece = models.OneToOneField(
        "Piece", on_delete=models.CASCADE, related_name="organization_relationship"
    )
    relationship_type = models.CharField(max_length=10, choices=RELATIONSHIP_TYPES)
    # Generic foreign key to any organization type
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    organization = GenericForeignKey("content_type", "object_id")
    # Common fields for all relationship types
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    # Field specific to rental relationship
    rental_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Only applicable to RENTED relationships.",
    )

    # Organization type mapping
    ORGANIZATION_TYPE_MAP = {
        RENTED: ("library.models.Rental_Organization", "a Rental Organization"),
        ON_LOAN: ("library.models.Loaning_Organization", "a Loaning Organization"),
        BORROWED: ("library.models.Borrowing_Organization", "a Borrowing Organization"),
    }

    def __str__(self):
        return f"{self.piece.title} - {self.get_relationship_type_display()} from {self.organization}"

    def clean(self):
        errors = {}
        self._validate_organization_type(errors)
        self._validate_rental_cost(errors)

        if errors:
            raise ValidationError(errors)

    def _validate_organization_type(self, errors):
        # Validate the organization type matches the relationship type
        org_class_path, org_name = self.ORGANIZATION_TYPE_MAP.get(
            self.relationship_type, (None, None)
        )
        if org_class_path:
            from django.apps import apps

            app_label, model_name = org_class_path.rsplit(".", 1)
            org_class = apps.get_model(app_label, model_name)
            if not isinstance(self.organization, org_class):
                errors["organization"] = [
                    f"Organization must be a {org_name} for {self.get_relationship_type_display()} relationships."
                ]

    def _validate_rental_cost(self, errors):
        # Only rental relationships should have rental cost
        if self.relationship_type != self.RENTED and self.rental_cost:
            errors["rental_cost"] = (
                "Rental cost is only applicable to RENTED relationships."
            )


"""The Organization models are for the rental, loaning, and borrowing organizations."""


class Organization(models.Model):
    name = models.CharField(max_length=100)
    contact_name = models.CharField(max_length=100, blank=True)
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        raise NotImplementedError("Subclasses must implement get_absolute_url().")

    class Meta:
        ordering = ["name"]
        abstract = True


class Rental_Organization(Organization):
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Rental Organizations"
        verbose_name = "Rental Organization"
        ordering = ["name"]

    def get_absolute_url(self):
        return reverse("rental_organization_detail", args=[str(self.id)])


class Loaning_Organization(Organization):
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Loaning Organizations"
        verbose_name = "Loaning Organization"
        ordering = ["name"]

    def get_absolute_url(self):
        return reverse("loaning_organization_detail", args=[str(self.id)])


class Borrowing_Organization(Organization):
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Borrowing Organizations"
        verbose_name = "Borrowing Organization"
        ordering = ["name"]

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

    # Miscellaneous info
    copyright_date = models.DateField(blank=True, null=True)
    purchase_date = models.DateField(blank=True, null=True)
    duration = models.DurationField(blank=True, null=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        errors = {}
        # Check relationship exists if status requires it
        if self.status in [
            PieceStatus.RENTED,
            PieceStatus.ON_LOAN,
            PieceStatus.BORROWED,
        ]:
            try:
                relationship = self.organization_relationship
                # Verify relationship type matches status
                if (
                    self.status == PieceStatus.RENTED
                    and relationship.relationship_type != PieceStatus.RENTED
                ):
                    errors["status"] = (
                        "Organization relationship type must be RENTED for RENTED status."
                    )
                if (
                    self.status == PieceStatus.ON_LOAN
                    and relationship.relationship_type != PieceStatus.ON_LOAN
                ):
                    errors["status"] = (
                        "Organization relationship type must be ON_LOAN for ON_LOAN status."
                    )
                if (
                    self.status == PieceStatus.BORROWED
                    and relationship.relationship_type != PieceStatus.BORROWED
                ):
                    errors["status"] = (
                        "Organization relationship type must be BORROWED for BORROWED status."
                    )
            except PieceOrganizationRelationship.DoesNotExist:
                errors["status"] = (
                    f"Pieces with {self.get_status_display()} status require an organization relationship."
                )
        # Conversely, if not a status that requires a relationship, shouldn't have one
        elif hasattr(self, "organization_relationship"):
            errors["status"] = (
                f"Pieces with {self.get_status_display()} status should not have an organization relationship."
            )
        if errors:
            raise ValidationError(errors)

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

    class Meta:
        ordering = ["title"]
        indexes = [
            models.Index(fields=["title"]),
        ]
