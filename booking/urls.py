from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('showtimes/<int:movie_id>/', views.showtimes, name='showtimes'),
]