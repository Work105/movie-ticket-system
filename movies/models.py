from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Movie(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    duration_minutes = models.IntegerField()
    poster_url = models.URLField(blank=True, null=True)
    genre = models.CharField(max_length=100)
    release_date = models.DateField()
    poster_url = models.URLField(blank=True, null=True)
    
    def __str__(self):
        return self.title

class Showtime(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='showtimes')
    show_date = models.DateField()
    show_time = models.TimeField()
    total_seats = models.IntegerField(default=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        unique_together = ['movie', 'show_date', 'show_time']
    
    def __str__(self):
        return f"{self.movie.title} - {self.show_date} {self.show_time}"

class Seat(models.Model):
    showtime = models.ForeignKey(Showtime, on_delete=models.CASCADE, related_name='seats')
    seat_number = models.CharField(max_length=5)  # e.g., "A1", "A2", "B1"
    is_booked = models.BooleanField(default=False)
    booked_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    booked_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ['showtime', 'seat_number']
    
    def __str__(self):
        status = "Booked" if self.is_booked else "Available"
        return f"{self.seat_number} - {status}"
