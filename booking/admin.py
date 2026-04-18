from django.contrib import admin
from .models import Movie, Theater, ShowTime, Booking

class MovieAdmin(admin.ModelAdmin):
    list_display = ['title', 'release_date', 'duration', 'genre']
    list_filter = ['release_date', 'genre']
    search_fields = ['title', 'description']
    ordering = ['-release_date']

class TheaterAdmin(admin.ModelAdmin):
    list_display = ['name', 'location', 'capacity']
    search_fields = ['name', 'location']

class ShowTimeAdmin(admin.ModelAdmin):
    list_display = ['movie', 'theater', 'date', 'time', 'seats_available', 'price']
    list_filter = ['date', 'theater', 'movie']
    search_fields = ['movie__title', 'theater__name']
    ordering = ['date', 'time']
    
    # Custom admin actions
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
        from datetime import date
        count = 0
        for showtime in queryset:
            if showtime.date >= date.today():
                count += 1
        self.message_user(request, f"{count} out of {queryset.count()} showtimes are upcoming")
    mark_as_upcoming.short_description = "Check which shows are upcoming"

class BookingAdmin(admin.ModelAdmin):
    list_display = ['user', 'showtime', 'seats', 'total_price', 'status', 'booked_at']
    list_filter = ['status', 'booked_at', 'showtime__movie']
    search_fields = ['user__username', 'showtime__movie__title']
    readonly_fields = ['booked_at', 'total_price']
    ordering = ['-booked_at']
    
    # Custom admin actions
    actions = ['confirm_bookings', 'cancel_bookings']
    
    def confirm_bookings(self, request, queryset):
        queryset.update(status='confirmed')
        self.message_user(request, f"Confirmed {queryset.count()} bookings")
    confirm_bookings.short_description = "Confirm selected bookings"
    
    def cancel_bookings(self, request, queryset):
        # Restore seats when cancelling from admin
        for booking in queryset:
            if booking.status == 'confirmed':
                booking.showtime.seats_available += booking.seats
                booking.showtime.save()
        queryset.update(status='cancelled')
        self.message_user(request, f"Cancelled {queryset.count()} bookings and restored seats")
    cancel_bookings.short_description = "Cancel selected bookings"

admin.site.register(Movie, MovieAdmin)
admin.site.register(Theater, TheaterAdmin)
admin.site.register(ShowTime, ShowTimeAdmin)
admin.site.register(Booking, BookingAdmin)