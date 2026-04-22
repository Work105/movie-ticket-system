from django.db import models
from django.contrib.auth.models import User


class Theatre(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=300)
    total_seats = models.IntegerField(default=100)

    def __str__(self):
        return self.name


class Movie(models.Model):
    GENRE_CHOICES = [
        ('action', 'Action'),
        ('comedy', 'Comedy'),
        ('drama', 'Drama'),
        ('horror', 'Horror'),
        ('sci_fi', 'Sci-Fi'),
        ('romance', 'Romance'),
        ('thriller', 'Thriller'),
    ]
    title = models.CharField(max_length=200)
    description = models.TextField()
    genre = models.CharField(max_length=100, choices=GENRE_CHOICES)
    duration_minutes = models.IntegerField()
    poster_url = models.URLField(blank=True, null=True)
    release_date = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Showtime(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='showtimes')
    theatre = models.ForeignKey(Theatre, on_delete=models.CASCADE, related_name='showtimes')
    show_date = models.DateField()
    show_time = models.TimeField()
    price = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        ordering = ['show_date', 'show_time']

    def __str__(self):
        return f"{self.movie.title} at {self.theatre.name} — {self.show_date} {self.show_time}"

    def available_seats(self):
        return self.seat_set.filter(is_booked=False).count()


class Seat(models.Model):
    ROW_CHOICES = [(r, r) for r in 'ABCDEFGHIJ']
    showtime = models.ForeignKey(Showtime, on_delete=models.CASCADE)
    row = models.CharField(max_length=1, choices=ROW_CHOICES)
    number = models.IntegerField()
    is_booked = models.BooleanField(default=False)

    class Meta:
        unique_together = ('showtime', 'row', 'number')
        ordering = ['row', 'number']

    def __str__(self):
        return f"{self.row}{self.number}"


class Booking(models.Model):
    STATUS_CHOICES = [
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    showtime = models.ForeignKey(Showtime, on_delete=models.CASCADE)
    seats = models.ManyToManyField(Seat)
    booked_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='confirmed')

    def __str__(self):
        return f"Booking #{self.id} by {self.user.username}"