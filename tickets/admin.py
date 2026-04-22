from django.contrib import admin
from django.utils.html import format_html
from .models import Theatre, Movie, Showtime, Seat, Booking


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    fields = ('title', 'description', 'genre', 'duration_minutes', 'release_date', 'poster_url', 'is_active')
    list_display = ('title', 'genre', 'duration_minutes', 'release_date', 'is_active', 'poster_preview')
    list_filter = ('genre', 'is_active')
    search_fields = ('title', 'genre')
    ordering = ('-release_date',)

    def poster_preview(self, obj):
        if obj.poster_url:
            return format_html('<img src="{}" style="height:60px; border-radius:6px;" />', obj.poster_url)
        return "No Poster"
    poster_preview.short_description = 'Poster'


@admin.register(Theatre)
class TheatreAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'total_seats')
    search_fields = ('name', 'location')


@admin.register(Showtime)
class ShowtimeAdmin(admin.ModelAdmin):
    list_display = ('movie', 'theatre', 'show_date', 'show_time', 'price', 'available_seats')
    list_filter = ('movie', 'theatre', 'show_date')
    search_fields = ('movie__title', 'theatre__name')
    ordering = ('show_date', 'show_time')


@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ('showtime', 'row', 'number', 'is_booked')
    list_filter = ('is_booked', 'row')


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'showtime', 'booked_at', 'total_price', 'status')
    list_filter = ('status',)
    search_fields = ('user__username',)