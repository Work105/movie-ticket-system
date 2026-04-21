from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from movies.models import Showtime, Movie

def home(request):
    # Get all movies (not just showtimes)
    movies = Movie.objects.all()
    
    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>CINEMA TICKET | Book Your Movie</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        <style>
            body {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }
            .navbar {
                background: rgba(0,0,0,0.9) !important;
            }
            .navbar-brand {
                font-size: 28px;
                font-weight: bold;
                color: #ff6b6b !important;
            }
            .hero {
                text-align: center;
                padding: 60px 20px;
                color: white;
            }
            .hero h1 {
                font-size: 48px;
                font-weight: bold;
            }
            .movie-card {
                background: white;
                border-radius: 15px;
                overflow: hidden;
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
                transition: transform 0.3s;
                height: 100%;
                margin-bottom: 30px;
            }
            .movie-card:hover {
                transform: translateY(-10px);
            }
            .poster-img {
                height: 350px;
                object-fit: cover;
                width: 100%;
            }
            .movie-info {
                padding: 20px;
            }
            .movie-title {
                font-size: 22px;
                font-weight: bold;
            }
            .genre {
                display: inline-block;
                background: #667eea;
                color: white;
                padding: 4px 12px;
                border-radius: 20px;
                font-size: 12px;
                margin-bottom: 10px;
            }
            .showtime-badge {
                background: #f0f0f0;
                padding: 8px 12px;
                border-radius: 10px;
                margin: 10px 0;
            }
            .price {
                font-size: 24px;
                font-weight: bold;
                color: #e74c3c;
            }
            .btn-book {
                background: linear-gradient(45deg, #667eea, #764ba2);
                border: none;
                padding: 10px 20px;
                font-weight: bold;
                color: white;
                border-radius: 8px;
                text-decoration: none;
                display: inline-block;
            }
            .btn-book:hover {
                transform: scale(1.02);
                color: white;
            }
            .action-buttons {
                text-align: center;
                margin: 40px 0;
            }
            .action-btn {
                margin: 0 10px;
                padding: 12px 30px;
                border-radius: 50px;
                font-weight: bold;
            }
            footer {
                background: rgba(0,0,0,0.8);
                color: white;
                text-align: center;
                padding: 20px;
                margin-top: 50px;
            }
        </style>
    </head>
    <body>
        <nav class="navbar navbar-dark">
            <div class="container">
                <a class="navbar-brand" href="/">
                    <i class="fas fa-film"></i> CINEMA TICKET
                </a>
            </div>
        </nav>
        
        <div class="hero">
            <div class="container">
                <h1><i class="fas fa-ticket-alt"></i> Book Your Movie Tickets</h1>
                <p>Experience the magic of cinema with our easy online booking system</p>
            </div>
        </div>
        
        <div class="container">
            <div class="row">
    '''
    
    # Show each movie with its first showtime
    for movie in movies:
        # Get the first showtime for this movie
        showtime = Showtime.objects.filter(movie=movie).first()
        
        # Poster URL
        poster = movie.poster_url if movie.poster_url else "https://via.placeholder.com/300x350?text=No+Poster"
        
        # Showtime details
        if showtime:
            show_date = showtime.show_date
            show_time = showtime.show_time
            price = showtime.price
            showtime_id = showtime.id
            total_seats = showtime.total_seats
        else:
            show_date = "Coming Soon"
            show_time = "TBA"
            price = "TBA"
            showtime_id = "#"
            total_seats = "0"
        
        html += f'''
            <div class="col-md-6 col-lg-4 mb-4">
                <div class="movie-card">
                    <img src="{poster}" class="poster-img" alt="{movie.title}" onerror="this.src='https://via.placeholder.com/300x350?text=No+Poster'">
                    <div class="movie-info">
                        <span class="genre"><i class="fas fa-tag"></i> {movie.genre}</span>
                        <h3 class="movie-title">{movie.title}</h3>
                        <p class="text-muted">{movie.description[:100]}...</p>
                        <div class="showtime-badge">
                            📅 {show_date} | 🕐 {show_time} | 🪑 {total_seats} seats
                        </div>
                        <div class="d-flex justify-content-between align-items-center mt-3">
                            <span class="price">Rs. {price}</span>
                            <a href="/bookings/select-seats/{showtime_id}/" class="btn-book">
                                <i class="fas fa-ticket-alt"></i> Book Now
                            </a>
                        </div>
                    </div>
                </div>
            </div>
        '''
    
    html += '''
            </div>
            
            <div class="action-buttons">
                <a href="/accounts/login/" class="btn btn-outline-light action-btn">
                    <i class="fas fa-sign-in-alt"></i> Login
                </a>
                <a href="/accounts/register/" class="btn btn-outline-light action-btn">
                    <i class="fas fa-user-plus"></i> Register
                </a>
                <a href="/bookings/booking-history/" class="btn btn-info action-btn">
                    <i class="fas fa-history"></i> My Bookings
                </a>
            </div>
        </div>
        
        <footer>
            <p>&copy; 2026 CINEMA TICKET | Business Application Development Assignment</p>
        </footer>
        
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    </body>
    </html>
    '''
    
    return HttpResponse(html)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('accounts/', include('accounts.urls')),
    path('bookings/', include('bookings.urls')),
]