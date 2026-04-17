from django.contrib import admin
from .models import Movie, Theater, ShowTime, Booking

admin.site.register(Movie)
admin.site.register(Theater)
admin.site.register(ShowTime)
admin.site.register(Booking)