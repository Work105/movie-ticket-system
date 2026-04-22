from django.contrib import admin
from django import forms
from django.core.exceptions import ValidationError
from .models import Movie, Theater, ShowTime, Booking
from datetime import date

# ========== CUSTOM FORM FOR SHOWTIME WITH VALIDATION ==========

class ShowTimeForm(forms.ModelForm):
    class Meta:
        model = ShowTime
        fields = '__all__'
    
    def clean_seats_available(self):
        seats = self.cleaned_data.get('seats_available')
        if seats < 0:
            raise ValidationError('❌ Seats available cannot be negative!')
        return seats
    
    def clean(self):
        cleaned_data = super().clean()
        seats_available = cleaned_data.get('seats_available')
        theater = cleaned_data.get('theater')
        show_date = cleaned_data.get('date')
        
        if theater and seats_available:
            if seats_available > theater.capacity:
                raise ValidationError({
                    'seats_available': f'❌ Cannot exceed theater capacity ({theater.capacity})!'
                })
        
        if show_date and show_date < date.today():
            raise ValidationError({
                'date': f'❌ Cannot create showtime for past date ({show_date})!'
            })
        
        return cleaned_data

# ========== CUSTOM FORM FOR BOOKING WITH VALIDATION ==========

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = '__all__'
    
    def clean_seats(self):
        seats = self.cleaned_data.get('seats')
        if seats <= 0:
            raise ValidationError('❌ Must book at least 1 seat!')
        if seats > 10:
            raise ValidationError('❌ Maximum 10 seats allowed per booking!')
        return seats
    
    def clean(self):
        cleaned_data = super().clean()
        seats = cleaned_data.get('seats')
        showtime = cleaned_data.get('showtime')
        
        if showtime and seats:
            if seats > showtime.seats_available:
                raise ValidationError({
                    'seats': f'❌ Only {showtime.seats_available} seats available!'
                })
        
        return cleaned_data

# ========== ADMIN CLASSES ==========

class MovieAdmin(admin.ModelAdmin):
    list_display = ['title', 'release_date', 'duration', 'genre']
    list_filter = ['release_date', 'genre']
    search_fields = ['title', 'description']
    ordering = ['-release_date']

class TheaterAdmin(admin.ModelAdmin):
    list_display = ['name', 'location', 'capacity']
    search_fields = ['name', 'location']

class ShowTimeAdmin(admin.ModelAdmin):
    form = ShowTimeForm
    list_display = ['movie', 'theater', 'date', 'time', 'seats_available', 'price']
    list_filter = ['date', 'theater', 'movie']
    search_fields = ['movie__title', 'theater__name']
    ordering = ['date', 'time']
    
    actions = ['increase_seats', 'decrease_seats', 'mark_as_upcoming']
    
    def increase_seats(self, request, queryset):
        for showtime in queryset:
            showtime.seats_available += 10
            showtime.save()
        self.message_user(request, f"Increased seats by 10 for {queryset.count()} showtimes")
    increase_seats.short_description = "Increase seats by 10"
    
    def decrease_seats(self, request, queryset):
        for showtime in queryset:
            if showtime.seats_available >= 10:
                showtime.seats_available -= 10
                showtime.save()
        self.message_user(request, f"Decreased seats by 10 for {queryset.count()} showtimes")
    decrease_seats.short_description = "Decrease seats by 10"
    
    def mark_as_upcoming(self, request, queryset):
        count = 0
        for showtime in queryset:
            if showtime.date >= date.today():
                count += 1
        self.message_user(request, f"{count} out of {queryset.count()} showtimes are upcoming")
    mark_as_upcoming.short_description = "Check which shows are upcoming"

class BookingAdmin(admin.ModelAdmin):
    form = BookingForm
    list_display = ['user', 'showtime', 'seats', 'total_price', 'status', 'booking_reference', 'booked_at']
    list_filter = ['status', 'booked_at', 'showtime__movie']
    search_fields = ['user__username', 'showtime__movie__title', 'booking_reference']
    readonly_fields = ['booked_at', 'total_price', 'booking_reference']
    ordering = ['-booked_at']
    
    actions = ['confirm_bookings', 'cancel_bookings']
    
    def confirm_bookings(self, request, queryset):
        queryset.update(status='confirmed')
        self.message_user(request, f"Confirmed {queryset.count()} bookings")
    confirm_bookings.short_description = "Confirm selected bookings"
    
    def cancel_bookings(self, request, queryset):
        for booking in queryset:
            if booking.status == 'confirmed':
                booking.showtime.seats_available += booking.seats
                booking.showtime.save()
        queryset.update(status='cancelled')
        self.message_user(request, f"Cancelled {queryset.count()} bookings and restored seats")
    cancel_bookings.short_description = "Cancel selected bookings"

# Register all models
admin.site.register(Movie, MovieAdmin)
admin.site.register(Theater, TheaterAdmin)
admin.site.register(ShowTime, ShowTimeAdmin)
admin.site.register(Booking, BookingAdmin)