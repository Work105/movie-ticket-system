from django.contrib import admin
from .models import Theatre, Movie, Showtime, Seat, Booking

@admin.register(Theatre)
class TheatreAdmin(admin.ModelAdmin):
    list_display = ['name', 'location', 'total_seats']

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['title', 'genre', 'duration_minutes', 'release_date', 'is_active']

@admin.register(Showtime)
class ShowtimeAdmin(admin.ModelAdmin):
    list_display = ['movie', 'theatre', 'show_date', 'show_time', 'price']

@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ['showtime', 'row', 'number', 'is_booked']

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'showtime', 'total_price', 'status']