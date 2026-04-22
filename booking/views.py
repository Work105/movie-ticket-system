from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.http import JsonResponse
from .models import Movie, ShowTime, Booking   
from datetime import date
from .utils import validate_booking_request, calculate_total_price, generate_booking_reference

# ========== HOME VIEW ==========

def home(request):
    """
    Display all movies on the home page.
    """
    movies = Movie.objects.all()
    return render(request, 'booking/home.html', {'movies': movies})

# ========== SHOWTIMES VIEW ==========

def showtimes(request, movie_id):
    """
    Display all showtimes for a specific movie.
    """
    movie = get_object_or_404(Movie, id=movie_id)
    showtimes = ShowTime.objects.filter(movie=movie)
    return render(request, 'booking/showtimes.html', {
        'movie': movie,
        'showtimes': showtimes,
        'today': date.today()
    })

# ========== REGISTER VIEW ==========

def register(request):
    """
    Handle user registration.
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        if password != confirm_password:
            messages.error(request, '❌ Passwords do not match.')
            return redirect('register')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, f'❌ Username "{username}" is already taken.')
            return redirect('register')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, f'❌ Email "{email}" is already registered.')
            return redirect('register')
        
        if len(password) < 6:
            messages.error(request, '❌ Password must be at least 6 characters.')
            return redirect('register')
        
        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        messages.success(request, f'✅ Welcome {username}!')
        return redirect('home')
    
    return render(request, 'booking/register.html')

# ========== LOGIN VIEW ==========

def user_login(request):
    """
    Handle user login authentication.
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if not username or not password:
            messages.error(request, '❌ Please enter both username and password.')
            return redirect('login')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'✅ Welcome back {username}!')
            return redirect('home')
        else:
            messages.error(request, '❌ Invalid username or password.')
    
    return render(request, 'booking/login.html')

# ========== LOGOUT VIEW ==========

def user_logout(request):
    """
    Handle user logout.
    """
    logout(request)
    messages.info(request, '✅ You have been successfully logged out.')
    return redirect('home')

# ========== BOOK TICKET VIEW ==========

@login_required
def book_ticket(request, showtime_id):
    """
    Handle ticket booking for a specific showtime.
    """
    showtime = get_object_or_404(ShowTime, id=showtime_id)
    
    # Prevent past bookings
    if showtime.date < date.today():
        messages.error(request, f'❌ Cannot book tickets for past showtimes!')
        return redirect('showtimes', movie_id=showtime.movie.id)
    
    # Prevent duplicate active bookings
    existing_booking = Booking.objects.filter(
        user=request.user, 
        showtime=showtime, 
        status='confirmed'
    ).exists()
    
    if existing_booking:
        messages.error(request, f'❌ You already have a confirmed booking for this show.')
        return redirect('showtimes', movie_id=showtime.movie.id)
    
    if request.method == 'POST':
        try:
            seats = int(request.POST.get('seats', 0))
            
            if seats <= 0:
                messages.error(request, '❌ Please select at least 1 seat.')
                return redirect('book_ticket', showtime_id=showtime_id)
            
            if seats > 10:
                messages.error(request, '❌ Maximum 10 seats allowed per booking.')
                return redirect('book_ticket', showtime_id=showtime_id)
            
            if not showtime.can_book(seats):
                messages.error(request, f'❌ Only {showtime.seats_available} seats available.')
                return redirect('book_ticket', showtime_id=showtime_id)
            
            with transaction.atomic():
                booking = Booking.objects.create(
                    user=request.user,
                    showtime=showtime,
                    seats=seats,
                    total_price=showtime.price * seats
                )
                showtime.seats_available -= seats
                showtime.save()
            
            messages.success(request, f'✅ Successfully booked {seats} ticket(s)! Reference: {booking.booking_reference}')
            return redirect('my_bookings')
            
        except ValueError:
            messages.error(request, '❌ Invalid number of seats.')
            return redirect('book_ticket', showtime_id=showtime_id)
    
    return render(request, 'booking/book_ticket.html', {'showtime': showtime})

# ========== MY BOOKINGS VIEW ==========

@login_required
def my_bookings(request):
    """
    Display user's booking history.
    """
    all_bookings = Booking.objects.filter(user=request.user).select_related(
        'showtime', 'showtime__movie', 'showtime__theater'
    ).order_by('-booked_at')
    
    upcoming_bookings = []
    past_bookings = []
    
    for booking in all_bookings:
        if booking.showtime.date >= date.today() and booking.status == 'confirmed':
            upcoming_bookings.append(booking)
        else:
            past_bookings.append(booking)
    
    if not all_bookings:
        messages.info(request, '📅 You have no bookings yet.')
    
    return render(request, 'booking/my_bookings.html', {
        'upcoming_bookings': upcoming_bookings,
        'past_bookings': past_bookings
    })

# ========== CANCEL BOOKING VIEW ==========

@login_required
def cancel_booking(request, booking_id):
    """
    Cancel an existing booking.
    """
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    if booking.status == 'cancelled':
        messages.warning(request, '⚠️ This booking was already cancelled.')
        return redirect('my_bookings')
    
    if booking.showtime.date < date.today():
        messages.error(request, '❌ Cannot cancel past bookings.')
        return redirect('my_bookings')
    
    with transaction.atomic():
        booking.showtime.seats_available += booking.seats
        booking.showtime.save()
        booking.status = 'cancelled'
        booking.save()
    
    messages.success(request, f'✅ Booking {booking.booking_reference} cancelled successfully.')
    return redirect('my_bookings')

# ========== NEW VIEWS FROM FRIEND'S SYSTEM ==========

@login_required
def check_availability(request, showtime_id):
    """AJAX endpoint to check seat availability"""
    showtime = get_object_or_404(ShowTime, id=showtime_id)
    requested_seats = int(request.GET.get('seats', 0))
    
    is_available = showtime.can_book(requested_seats)
    
    return JsonResponse({
        'available': is_available,
        'seats_left': showtime.seats_available,
        'max_bookable': min(10, showtime.seats_available)
    })

@login_required
def booking_details(request, booking_id):
    """View detailed booking information (for ticket printing)"""
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    return render(request, 'booking/booking_details.html', {
        'booking': booking,
        'qr_data': f"BOOKING:{booking.booking_reference}:{booking.showtime.id}:{booking.seats}"
    })

@login_required
def my_tickets(request):
    """View all tickets (alternative view)"""
    bookings = Booking.objects.filter(user=request.user).select_related(
        'showtime', 'showtime__movie', 'showtime__theater'
    ).order_by('-booked_at')
    
    return render(request, 'booking/my_tickets.html', {'bookings': bookings})