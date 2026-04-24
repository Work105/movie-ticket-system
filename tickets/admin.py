from django.contrib import admin
from django import forms
from django.core.exceptions import ValidationError
from django.utils.html import format_html
from .models import Theatre, Movie, Showtime, Seat, Booking

# ========== CUSTOM FORM FOR THEATRE WITH VALIDATION ==========

class TheatreForm(forms.ModelForm):
    class Meta:
        model = Theatre
        fields = '__all__'
    
    def clean_total_seats(self):
        seats = self.cleaned_data.get('total_seats')
        if seats < 0:
            raise ValidationError('❌ Total seats cannot be negative! Please enter a positive number.')
        if seats == 0:
            raise ValidationError('⚠️ Theatre must have at least 1 seat.')
        return seats

# ========== CUSTOM FORM FOR SHOWTIME WITH VALIDATION ==========

class ShowtimeForm(forms.ModelForm):
    class Meta:
        model = Showtime
        fields = '__all__'
    
    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price < 0:
            raise ValidationError('❌ Price cannot be negative!')
        return price

# ========== ADMIN CLASSES ==========

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
    form = TheatreForm  # ADD THIS LINE for validation
    list_display = ('name', 'location', 'total_seats')
    search_fields = ('name', 'location')


@admin.register(Showtime)
class ShowtimeAdmin(admin.ModelAdmin):
    form = ShowtimeForm  # ADD THIS LINE for validation
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