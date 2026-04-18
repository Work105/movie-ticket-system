from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from .models import Movie, ShowTime, Booking   
from datetime import date

# ========== HOME VIEW ==========

def home(request):
    """
    Display all movies on the home page.
    Retrieves all movies from database and passes to template.
    """
    movies = Movie.objects.all()
    return render(request, 'booking/home.html', {'movies': movies})

# ========== SHOWTIMES VIEW ==========

def showtimes(request, movie_id):
    """
    Display all showtimes for a specific movie.
    Args: movie_id - ID of the selected movie
    """
    movie = get_object_or_404(Movie, id=movie_id)
    showtimes = ShowTime.objects.filter(movie=movie)
    return render(request, 'booking/showtimes.html', {
        'movie': movie,
        'showtimes': showtimes
    })

# ========== REGISTER VIEW ==========

def register(request):
    """
    Handle user registration.
    Validates username, email, password and creates new user account.
    Automatically logs in user after successful registration.
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return redirect('register')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('register')
        
        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        messages.success(request, f'Welcome {username}!')
        return redirect('home')
    
    return render(request, 'booking/register.html')

# ========== LOGIN VIEW ==========

def user_login(request):
    """
    Handle user login authentication.
    Authenticates username and password, creates session for logged in user.
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back {username}!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')
    
    return render(request, 'booking/login.html')

# ========== LOGOUT VIEW ==========

def user_logout(request):
    """
    Handle user logout.
    Ends user session and redirects to home page.
    """
    logout(request)
    messages.info(request, 'You have been logged out')
    return redirect('home')

# ========== BOOK TICKET VIEW ==========

@login_required
def book_ticket(request, showtime_id):
    """
    Handle ticket booking for a specific showtime.
    Validates: past dates, duplicate bookings, seat availability.
    Uses atomic transaction to ensure data consistency.
    """
    showtime = get_object_or_404(ShowTime, id=showtime_id)
    
    # Prevent past bookings
    if showtime.date < date.today():
        messages.error(request, f'Cannot book tickets for past showtimes!')
        return redirect('showtimes', movie_id=showtime.movie.id)
    
    # Prevent duplicate active bookings
    existing_booking = Booking.objects.filter(
        user=request.user, 
        showtime=showtime, 
        status='confirmed'
    ).exists()
    
    if existing_booking:
        messages.error(request, 'You already have a booking for this showtime!')
        return redirect('showtimes', movie_id=showtime.movie.id)
    
    if request.method == 'POST':
        try:
            seats = int(request.POST.get('seats', 0))
            
            if seats <= 0:
                messages.error(request, 'Please select at least 1 seat')
                return redirect('book_ticket', showtime_id=showtime_id)
            
            if not showtime.can_book(seats):
                messages.error(request, f'Only {showtime.seats_available} seats available')
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
            
            messages.success(request, f'Booked {seats} ticket(s)! Total: ${booking.total_price}')
            return redirect('my_bookings')
            
        except ValueError:
            messages.error(request, 'Invalid number of seats')
    
    return render(request, 'booking/book_ticket.html', {'showtime': showtime})

# ========== MY BOOKINGS VIEW ==========

@login_required
def my_bookings(request):
    """
    Display user's booking history.
    Separates bookings into upcoming and past for better UI.
    """
    all_bookings = Booking.objects.filter(user=request.user).select_related(
        'showtime', 'showtime__movie', 'showtime__theater'
    ).order_by('-booked_at')
    
    # Separate upcoming and past bookings
    upcoming_bookings = []
    past_bookings = []
    
    for booking in all_bookings:
        if booking.showtime.date >= date.today() and booking.status == 'confirmed':
            upcoming_bookings.append(booking)
        else:
            past_bookings.append(booking)
    
    return render(request, 'booking/my_bookings.html', {
        'upcoming_bookings': upcoming_bookings,
        'past_bookings': past_bookings
    })

# ========== CANCEL BOOKING VIEW ==========

@login_required
def cancel_booking(request, booking_id):
    """
    Cancel an existing booking.
    Restores seats to showtime and updates booking status.
    Uses atomic transaction to ensure data consistency.
    """
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    if booking.status == 'cancelled':
        messages.warning(request, 'Booking already cancelled')
        return redirect('my_bookings')
    
    with transaction.atomic():
        booking.showtime.seats_available += booking.seats
        booking.showtime.save()
        booking.status = 'cancelled'
        booking.save()
    
    messages.success(request, f'Booking cancelled. {booking.seats} seats restored.')
    return redirect('my_bookings')