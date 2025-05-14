# concerts/models.py

from django.db import models
from django.urls import reverse
from library.models import PersonBase


# Create your models here.
# PersonBase is defined in library/models.py
class Conductor(PersonBase):
    middle_initial = models.CharField(max_length=1, blank=True)
    honorific = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)

    def get_absolute_url(self):
        return reverse("conductor_detail", args=[str(self.id)])

    class Meta:
        verbose_name = "Conductor"
        verbose_name_plural = "Conductors"


class Guest(PersonBase):
    description = models.TextField(blank=True)

    def get_absolute_url(self):
        return reverse("guest_detail", args=[str(self.id)])

    class Meta:
        verbose_name = "Guest"
        verbose_name_plural = "Guests"


class Venue(models.Model):
    name = models.CharField(max_length=100)
    contact_name = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=2, blank=True)
    zip_code = models.CharField(max_length=5, blank=True)
    phone = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("venue_detail", args=[str(self.id)])

    class Meta:
        ordering = ["name"]


def concert_poster_upload_path(instance, filename):
    # This will save posters in MEDIA_ROOT/posters/<concert_id>/<filename>
    return f"posters/concert_{instance.id}/{filename}"


class Concert(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
    conductor = models.ManyToManyField(Conductor, blank=True)
    guests = models.ManyToManyField(Guest, blank=True)
    description = models.TextField(blank=True)
    poster = models.ImageField(
        upload_to="posters/",
        blank=True,
        null=True,
    )
