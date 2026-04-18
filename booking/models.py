from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import date, time as datetime_time
from django.utils import timezone

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
        ordering = ['-release_date']  # Newest movies first


class Theater(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    capacity = models.IntegerField(default=100, help_text="Total seats in theater")
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']  # Alphabetical order by name


class ShowTime(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='showtimes')
    theater = models.ForeignKey(Theater, on_delete=models.CASCADE, related_name='showtimes')
    date = models.DateField()
    time = models.TimeField()
    seats_available = models.IntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2, default=12.00)
    
    def __str__(self):
        return f"{self.movie.title} - {self.date} {self.time} at {self.theater.name}"
    
    def is_upcoming(self):
        """
        Check if showtime is in the future.
        Returns True if show date is today or in the future.
        """
        from datetime import date
        return self.date >= date.today()
    
    def can_book(self, requested_seats):
        """Check if requested seats are available"""
        return self.seats_available >= requested_seats and self.is_upcoming()
    
    class Meta:
        ordering = ['date', 'time']  # Earliest shows first


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
    
    def save(self, *args, **kwargs):
        # Calculate total price before saving
        if not self.total_price and self.showtime:
            self.total_price = self.showtime.price * self.seats
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.user.username} - {self.showtime.movie.title} ({self.seats} seats)"
    
    class Meta:
        ordering = ['-booked_at']  # Most recent bookings first