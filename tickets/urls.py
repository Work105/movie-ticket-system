from django.urls import path
from . import views
from django.urls import path
from . import views

urlpatterns = [
    path('', views.test_view, name='test'),
]


urlpatterns = [
    path('download-ticket/<int:booking_id>/', views.download_ticket, name='download_ticket'),
]
