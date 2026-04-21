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
            messages.error(request, '❌ Passwords do not match. Please re-enter your password.')
            return redirect('register')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, f'❌ Username "{username}" is already taken. Please choose a different username.')
            return redirect('register')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, f'❌ Email "{email}" is already registered. Please use a different email or login.')
            return redirect('register')
        
        if len(password) < 6:
            messages.error(request, '❌ Password must be at least 6 characters long for security.')
            return redirect('register')
        
        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        messages.success(request, f'✅ Welcome {username}! Your account has been created successfully.')
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
        
        if not username or not password:
            messages.error(request, '❌ Please enter both username and password.')
            return redirect('login')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'✅ Welcome back {username}! You are now logged in.')
            return redirect('home')
        else:
            messages.error(request, '❌ Invalid username or password. Please try again or register a new account.')
    
    return render(request, 'booking/login.html')

# ========== LOGOUT VIEW ==========

def user_logout(request):
    """
    Handle user logout.
    Ends user session and redirects to home page.
    """
    logout(request)
    messages.info(request, '✅ You have been successfully logged out. Come back soon!')
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
        messages.error(request, f'❌ Cannot book tickets for past showtimes! This show was on {showtime.date}. Please select a future show.')
        return redirect('showtimes', movie_id=showtime.movie.id)
    
    # Prevent duplicate active bookings
    existing_booking = Booking.objects.filter(
        user=request.user, 
        showtime=showtime, 
        status='confirmed'
    ).exists()
    
    if existing_booking:
        messages.error(request, f'❌ You already have a confirmed booking for {showtime.movie.title} on {showtime.date}. You cannot book the same show twice.')
        return redirect('showtimes', movie_id=showtime.movie.id)
    
    if request.method == 'POST':
        try:
            seats = int(request.POST.get('seats', 0))
            
            if seats <= 0:
                messages.error(request, '❌ Please select at least 1 seat to book.')
                return redirect('book_ticket', showtime_id=showtime_id)
            
            if seats > 10:
                messages.error(request, '❌ Maximum 10 seats allowed per booking. Please reduce the number of seats.')
                return redirect('book_ticket', showtime_id=showtime_id)
            
            if not showtime.can_book(seats):
                messages.error(request, f'❌ Only {showtime.seats_available} seats available for this showtime. Please select fewer seats.')
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
            
            messages.success(request, f'✅ Successfully booked {seats} ticket(s) for {showtime.movie.title}! Total: ${booking.total_price}. Enjoy the show!')
            return redirect('my_bookings')
            
        except ValueError:
            messages.error(request, '❌ Invalid number of seats. Please enter a valid number.')
            return redirect('book_ticket', showtime_id=showtime_id)
    
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
    
    if not all_bookings:
        messages.info(request, '📅 You have no bookings yet. Book a movie ticket to get started!')
    
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
        messages.warning(request, f'⚠️ This booking for {booking.showtime.movie.title} was already cancelled previously.')
        return redirect('my_bookings')
    
    # Check if showtime hasn't passed
    if booking.showtime.date < date.today():
        messages.error(request, f'❌ Cannot cancel past bookings for {booking.showtime.movie.title} because the show has already happened.')
        return redirect('my_bookings')
    
    with transaction.atomic():
        booking.showtime.seats_available += booking.seats
        booking.showtime.save()
        booking.status = 'cancelled'
        booking.save()
    
    messages.success(request, f'✅ Booking for {booking.showtime.movie.title} cancelled successfully. {booking.seats} seat(s) have been restored.')
    return redirect('my_bookings')