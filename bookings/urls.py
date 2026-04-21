from django.urls import path
from . import views

urlpatterns = [
    path('select-seats/<int:showtime_id>/', views.select_seats, name='select_seats'),
    path('confirm-booking/<int:showtime_id>/', views.confirm_booking, name='confirm_booking'),
    path('complete-booking/', views.complete_booking, name='complete_booking'),
    path('booking-history/', views.booking_history, name='booking_history'),
    path('cancel-booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
]