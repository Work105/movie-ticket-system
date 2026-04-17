from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from .models import Movie, ShowTime, Booking


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