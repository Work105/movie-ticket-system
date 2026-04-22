from django.urls import path
from . import views

urlpatterns = [
    # Public URLs
    path('', views.home, name='home'),
    path('showtimes/<int:movie_id>/', views.showtimes, name='showtimes'),
    
    # Authentication URLs
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    
    # Booking URLs
    path('book/<int:showtime_id>/', views.book_ticket, name='book_ticket'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('cancel/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    
    # NEW URLs FROM FRIEND'S SYSTEM
    path('check-availability/<int:showtime_id>/', views.check_availability, name='check_availability'),
    path('booking-details/<int:booking_id>/', views.booking_details, name='booking_details'),
    path('my-tickets/', views.my_tickets, name='my_tickets'),
]