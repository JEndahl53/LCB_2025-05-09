from django.contrib import admin

from .models import Conductor, Guest, Venue

admin.site.register(Conductor)
admin.site.register(Guest)
admin.site.register(Venue)
