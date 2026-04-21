from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from .forms import CustomUserCreationForm

@csrf_protect
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"🎉 Welcome {user.username}! Your account has been created successfully.")
            
            if user.role == 'admin':
                return redirect('admin_dashboard')
            else:
                return redirect('customer_dashboard')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'accounts/register.html', {'form': form})

@csrf_protect
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, f"Welcome back {user.username}!")
            if user.role == 'admin':
                return redirect('admin_dashboard')
            else:
                return redirect('customer_dashboard')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'accounts/login.html')

def user_logout(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')

@login_required
def customer_dashboard(request):
    return render(request, 'accounts/customer_dashboard.html', {'user': request.user})

@login_required
def admin_dashboard(request):
    from movies.models import Movie, Showtime
    from bookings.models import Booking
    
    context = {
        'user': request.user,
        'movie_count': Movie.objects.count(),
        'showtime_count': Showtime.objects.count(),
        'booking_count': Booking.objects.count(),
    }
    return render(request, 'accounts/admin_dashboard.html', context)