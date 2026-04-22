from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import date, time as datetime_time
from django.utils import timezone
import random
import string

class Movie(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    duration = models.IntegerField(help_text="Duration in minutes")
    release_date = models.DateField()
    poster_url = models.URLField(blank=True, null=True)
    genre = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-release_date']


class Theater(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    capacity = models.IntegerField(default=100, help_text="Total seats in theater")
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']


class ShowTime(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='showtimes')
    theater = models.ForeignKey(Theater, on_delete=models.CASCADE, related_name='showtimes')
    date = models.DateField()
    time = models.TimeField()
    seats_available = models.IntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2, default=12.00)
    
    def clean(self):
        """Validate showtime data"""
        if self.seats_available < 0:
            raise ValidationError({'seats_available': 'Seats available cannot be negative'})
        if self.seats_available > self.theater.capacity:
            raise ValidationError({'seats_available': f'Cannot exceed theater capacity ({self.theater.capacity})'})
        if self.date < date.today():
            raise ValidationError({'date': 'Cannot create showtime for past date'})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.movie.title} - {self.date} {self.time} at {self.theater.name}"
    
    def is_upcoming(self):
        from datetime import date
        return self.date >= date.today()
    
    def can_book(self, requested_seats):
        return self.seats_available >= requested_seats and self.is_upcoming()
    
    class Meta:
        ordering = ['date', 'time']


class Booking(models.Model):
    STATUS_CHOICES = [
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('expired', 'Expired'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    showtime = models.ForeignKey(ShowTime, on_delete=models.CASCADE, related_name='bookings')
    seats = models.IntegerField()
    total_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='confirmed')
    booked_at = models.DateTimeField(auto_now_add=True)
    
    # NEW FIELDS FROM FRIEND'S SYSTEM
    booking_reference = models.CharField(max_length=10, unique=True, editable=False, blank=True, null=True)
    qr_code = models.TextField(blank=True, null=True)
    payment_id = models.CharField(max_length=100, blank=True, null=True)
    
    def clean(self):
        """Validate booking data"""
        if self.seats <= 0:
            raise ValidationError({'seats': 'Must book at least 1 seat'})
        if self.seats > 10:
            raise ValidationError({'seats': 'Maximum 10 seats per booking'})
        if self.showtime and self.seats > self.showtime.seats_available:
            raise ValidationError({'seats': f'Only {self.showtime.seats_available} seats available'})

    def save(self, *args, **kwargs):
        # Generate unique booking reference if not exists
        if not self.booking_reference:
            import random
            import string
            self.booking_reference = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        
        # Calculate total price before saving
        if not self.total_price and self.showtime:
            self.total_price = self.showtime.price * self.seats
        
        self.full_clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.user.username} - {self.showtime.movie.title} ({self.seats} seats) - {self.booking_reference}"
    
    class Meta:
        ordering = ['-booked_at']