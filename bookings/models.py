from django.db import models
from django.contrib.auth import get_user_model
from movies.models import Showtime, Seat

User = get_user_model()

class Booking(models.Model):
    STATUS_CHOICES = (
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('expired', 'Expired'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    showtime = models.ForeignKey(Showtime, on_delete=models.CASCADE)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='confirmed')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        unique_together = ['showtime', 'seat']  # Prevent double booking
    
    def __str__(self):
        return f"{self.user.username} - {self.seat.seat_number}"
