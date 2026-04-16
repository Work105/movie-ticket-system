from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

def home(request):
    return HttpResponse("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Movie Ticket System</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body>
        <div class="container mt-5">
            <h1>🎬 Movie Ticket System</h1>
            <div class="row mt-4">
                <div class="col-md-4">
                    <div class="card">
                        <div class="card-body">
                            <h3>Avatar: The Way of Water</h3>
                            <p>Date: April 25, 2026</p>
                            <p>Time: 7:00 PM</p>
                            <p>Price: Rs. 500</p>
                            <a href="/bookings/select-seats/2/" class="btn btn-primary">Book Tickets</a>
                        </div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="card">
                        <div class="card-body">
                            <h3>Avatar: The Way of Water</h3>
                            <p>Date: April 25, 2026</p>
                            <p>Time: 9:00 PM</p>
                            <p>Price: Rs. 500</p>
                            <a href="/bookings/select-seats/3/" class="btn btn-primary">Book Tickets</a>
                        </div>
                    </div>
                </div>
            </div>
            <div class="mt-4">
                <a href="/accounts/login/" class="btn btn-secondary">Login</a>
                <a href="/accounts/register/" class="btn btn-secondary">Register</a>
                <a href="/bookings/booking-history/" class="btn btn-info">My Bookings</a>
            </div>
        </div>
    </body>
    </html>
    """)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('accounts/', include('accounts.urls')),
    path('bookings/', include('bookings.urls')),
]