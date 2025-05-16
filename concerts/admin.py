from django.contrib import admin

from .models import Conductor, Guest, Venue, Concert

admin.site.register(Conductor)
admin.site.register(Guest)
admin.site.register(Venue)
admin.site.register(Concert)
