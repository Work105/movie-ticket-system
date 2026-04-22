from django.contrib import admin
from django.utils.html import format_html
from .models import Movie, Showtime, Seat


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    # Fields shown in add/edit form
    fields = ('title', 'description', 'genre', 'duration_minutes', 'release_date', 'poster_url', 'is_active')

    # Columns shown in the movie list
    list_display = ('title', 'genre', 'duration_minutes', 'release_date', 'is_active', 'poster_preview')

    # Filter sidebar on the right
    list_filter = ('genre', 'is_active', 'release_date')

    # Search bar at the top
    search_fields = ('title', 'genre', 'description')

    # Default ordering
    ordering = ('-release_date',)

    # Show poster thumbnail in the list page
    def poster_preview(self, obj):
        if obj.poster_url:
            return format_html('<img src="{}" style="height:60px; border-radius:6px; box-shadow: 0 2px 6px rgba(0,0,0,0.3);" />', obj.poster_url)
        return "No Poster"
    poster_preview.short_description = 'Poster Preview'


@admin.register(Showtime)
class ShowtimeAdmin(admin.ModelAdmin):
    list_display = ('movie', 'show_date', 'show_time', 'total_seats', 'price')
    list_filter = ('movie', 'show_date')
    search_fields = ('movie__title',)
    ordering = ('show_date', 'show_time')


@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ('seat_number', 'showtime', 'is_booked', 'booked_by', 'booked_at')
    list_filter = ('is_booked', 'showtime')
    search_fields = ('seat_number', 'showtime__movie__title')
    ordering = ('showtime', 'seat_number')


