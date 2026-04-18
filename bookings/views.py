from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from movies.models import Showtime, Seat
from .utils import check_seat_availability, validate_booking, create_booking
from .models import Booking

@login_required
def select_seats(request, showtime_id):
        from movies.models import Showtime, Seat
        
        try:
            showtime = Showtime.objects.get(id=showtime_id)
            all_seats = Seat.objects.filter(showtime=showtime)
            
            # Get lists of seat numbers
            booked_seat_numbers = [seat.seat_number for seat in all_seats if seat.is_booked]
            available_seat_numbers = [seat.seat_number for seat in all_seats if not seat.is_booked]
            
        except Showtime.DoesNotExist:
            messages.error(request, "Showtime not found!")
            return redirect('booking_history')
        
        context = {
            'showtime': showtime,
            'available_seat_numbers': available_seat_numbers,
            'booked_seat_numbers': booked_seat_numbers,
        }
        return render(request, 'bookings/select_seats.html', context)

@login_required
def confirm_booking(request, showtime_id):
    if request.method == 'POST':
        seat_numbers = request.POST.getlist('seats')
        
        if not seat_numbers:
            messages.error(request, "Please select at least one seat")
            return redirect('select_seats', showtime_id=showtime_id)
        
        from movies.models import Showtime, Seat
        from .utils import validate_booking
        
        is_valid, message, available_seats = validate_booking(
            request, showtime_id, seat_numbers
        )
        
        if not is_valid:
            messages.error(request, message)
            return redirect('select_seats', showtime_id=showtime_id)
        
        showtime = Showtime.objects.get(id=showtime_id)
        total_price = showtime.price * len(available_seats)
        
        # Store in session
        request.session['pending_booking'] = {
            'showtime_id': showtime_id,
            'seat_ids': [seat.id for seat in available_seats],
            'total_price': str(total_price),
        }
        
        context = {
            'showtime': showtime,
            'seats': available_seats,
            'total_price': total_price,
        }
        return render(request, 'bookings/confirm_booking.html', context)
    
    return redirect('select_seats', showtime_id=showtime_id)

@login_required
def complete_booking(request):
    pending = request.session.get('pending_booking')
    
    if not pending:
        messages.error(request, "No pending booking found")
        return redirect('movie_list')
    
    success, message, bookings = create_booking(
        request,
        pending['showtime_id'],
        pending['seat_ids'],
        float(pending['total_price'])
    )
    
    if success:
        messages.success(request, message)
        del request.session['pending_booking']
        return redirect('booking_history')
    else:
        messages.error(request, message)
        return redirect('movie_list')

@login_required
def booking_history(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-booking_date')
    
    # Calculate total amount and total tickets
    total_amount = 0
    total_tickets = 0
    
    for booking in bookings:
        if booking.status == 'confirmed':
            total_amount += float(booking.total_price)
            total_tickets += 1
    
    context = {
        'bookings': bookings,
        'total_amount': total_amount,
        'total_tickets': total_tickets,
    }
    return render(request, 'bookings/booking_history.html', context)

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    if booking.status == 'cancelled':
        messages.warning(request, "Booking already cancelled")
    else:
        # Free up the seat
        seat = booking.seat
        seat.is_booked = False
        seat.booked_by = None
        seat.booked_at = None
        seat.save()
        
        # Update booking status
        booking.status = 'cancelled'
        booking.save()
        
        messages.success(request, f"Booking for seat {seat.seat_number} cancelled successfully")
    
    return redirect('booking_history')
