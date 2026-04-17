from django.shortcuts import render
from .models import Movie

def home(request):
    movies = Movie.objects.all()
    return render(request, 'booking/home.html', {'movies': movies})

from .models import Movie, ShowTime

def showtimes(request, movie_id):
    movie = Movie.objects.get(id=movie_id)
    showtimes = ShowTime.objects.filter(movie=movie)

    return render(request, 'booking/showtimes.html', {
        'movie': movie,
        'showtimes': showtimes
    })