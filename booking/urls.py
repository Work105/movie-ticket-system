from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.home, name='home'),
    path('showtimes/<int:movie_id>/', views.showtimes, name='showtimes'),
    
    # Authentication URLs 
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
]