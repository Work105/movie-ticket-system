from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from .models import Movie, ShowTime, Booking   
from datetime import date

def home(request):
    movies = Movie.objects.all()
    return render(request, 'booking/home.html', {'movies': movies})

def showtimes(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    showtimes = ShowTime.objects.filter(movie=movie)
    return render(request, 'booking/showtimes.html', {
        'movie': movie,
        'showtimes': showtimes
    })

# ========== REGISTER VIEW ==========

def register(request):
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

# ========== LOGIN & LOGOUT VIEWS ==========

def user_login(request):
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

def user_logout(request):
    logout(request)
    messages.info(request, 'You have been logged out')
    return redirect('home')

# ========== BOOK TICKET VIEW ==========

@login_required
def book_ticket(request, showtime_id):
    showtime = get_object_or_404(ShowTime, id=showtime_id)
    
    # SIMPLE DATE COMPARISON - THIS WILL WORK
    today = date.today()
    
    if showtime.date < today:
        messages.error(request, f'Cannot book tickets for past showtimes! (Show date: {showtime.date}, Today: {today})')
        return redirect('showtimes', movie_id=showtime.movie.id)
    
    if request.method == 'POST':
        try:
            seats = int(request.POST.get('seats', 0))
            if seats > 10:
                messages.error(request, 'Maximum 10 seats allowed per booking')
                return redirect('book_ticket', showtime_id=showtime_id)
            
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
    from datetime import date
    
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