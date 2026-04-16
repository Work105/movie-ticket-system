from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome {user.username}!")
            if user.role == 'admin':
                return redirect('admin_dashboard')
            else:
                return redirect('customer_dashboard')
        else:
            messages.error(request, "Please correct the errors.")
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'accounts/register.html', {'form': form})  # ← FIXED INDENTATION

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
    
    return render(request, 'accounts/login.html')  # ← FIXED: added 'accounts/'

def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def customer_dashboard(request):
    return render(request, 'accounts/customer_dashboard.html', {'user': request.user})  # ← FIXED: added 'accounts/'

@login_required
def admin_dashboard(request):
    return render(request, 'accounts/admin_dashboard.html', {'user': request.user})  # ← FIXED: added 'accounts/'