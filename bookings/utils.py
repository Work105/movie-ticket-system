from datetime import datetime
from django.utils import timezone
from django.contrib import messages
from .models import Booking
from movies.models import Seat, Showtime

def check_seat_availability(showtime_id, seat_number):
    """
    Check if a specific seat is available for a showtime
    Returns: (is_available, message, seat_object)
    """
    from movies.models import Seat
    
    try:
        seat = Seat.objects.get(showtime_id=showtime_id, seat_number=seat_number)
        
        if seat.is_booked:
            return False, f"Seat {seat_number} is already booked!", seat
        else:
            return True, f"Seat {seat_number} is available", seat
    except Seat.DoesNotExist:
        return False, f"Seat {seat_number} does not exist for this showtime", None

def validate_booking(request, showtime_id, seat_numbers):
    """
    Main validation function for booking
    Returns: (is_valid, error_message, available_seats)
    """
    errors = []
    available_seats = []
    
    # Check if user is logged in
    if not request.user.is_authenticated:
        return False, "Please login to book tickets", []
    
    # Check if showtime exists
    try:
        showtime = Showtime.objects.get(id=showtime_id)
    except Showtime.DoesNotExist:
        return False, "Showtime not found", []
    
    # Check if showtime is in the future
    show_datetime = datetime.combine(showtime.show_date, showtime.show_time)
    if show_datetime < datetime.now():
        return False, "Cannot book tickets for past showtimes", []
    
    # Check each seat
    for seat_number in seat_numbers:
        is_available, message, seat = check_seat_availability(showtime_id, seat_number)
        if is_available:
            available_seats.append(seat)
        else:
            errors.append(message)
    
    if errors:
        return False, " | ".join(errors), []
    
    return True, "All seats available!", available_seats

def create_booking(request, showtime_id, seat_ids, total_price):
    """
    Create a booking for the user
    Returns: (success, message, booking_objects)
    """
    from .models import Booking
    
    bookings = []
    
    for seat_id in seat_ids:
        seat = Seat.objects.get(id=seat_id)
        
        # Double-check seat is still available
        if seat.is_booked:
            return False, f"Seat {seat.seat_number} was just booked by someone else!", []
        
        # Create booking
        booking = Booking.objects.create(
            user=request.user,
            showtime_id=showtime_id,
            seat=seat,
            total_price=total_price / len(seat_ids),  # Divide price per seat
            status='confirmed'
        )
        
        # Mark seat as booked
        seat.is_booked = True
        seat.booked_by = request.user
        seat.booked_at = timezone.now()
        seat.save()
        
        bookings.append(booking)
    
    return True, f"Successfully booked {len(bookings)} seat(s)!", bookings