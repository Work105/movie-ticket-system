from datetime import datetime
from django.utils import timezone
from django.contrib import messages
from .models import Booking, ShowTime
import random
import string

def generate_booking_reference():
    """Generate a unique booking reference number"""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

def check_seat_availability(showtime, requested_seats):
    """
    Check if requested number of seats are available
    Returns: (is_available, message, available_count)
    """
    if showtime.seats_available >= requested_seats:
        return True, f"{requested_seats} seats available", showtime.seats_available
    else:
        return False, f"Only {showtime.seats_available} seats available", showtime.seats_available

def validate_booking_request(request, showtime, requested_seats):
    """
    Comprehensive booking validation
    Returns: (is_valid, error_message)
    """
    # Check if user is logged in
    if not request.user.is_authenticated:
        return False, "Please login to book tickets"
    
    # Check if showtime exists
    if not showtime:
        return False, "Showtime not found"
    
    # Check if showtime is in the future
    from datetime import datetime
    show_datetime = datetime.combine(showtime.date, showtime.time)
    if show_datetime < datetime.now():
        return False, "Cannot book tickets for past showtimes"
    
    # Check seat availability
    if not showtime.can_book(requested_seats):
        return False, f"Only {showtime.seats_available} seats available"
    
    # Check duplicate booking
    if Booking.objects.filter(user=request.user, showtime=showtime, status='confirmed').exists():
        return False, "You already have a booking for this show"
    
    return True, "Valid booking request"

def calculate_total_price(showtime, seats):
    """Calculate total price for booking"""
    return showtime.price * seats