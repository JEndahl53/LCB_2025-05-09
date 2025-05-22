from django.contrib import admin

from library.models import (
    Genre,
    Composer,
    Arranger,
    Piece,
    Rental_Organization,
    Loaning_Organization,
    Borrowing_Organization,
)

# Register your models here.
admin.site.register(Genre)
admin.site.register(Composer)
admin.site.register(Arranger)
admin.site.register(Piece)
admin.site.register(Rental_Organization)
admin.site.register(Loaning_Organization)
admin.site.register(Borrowing_Organization)
