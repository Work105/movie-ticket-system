from django.contrib.auth import get_user_model
from tickets.models import Movie
from datetime import date

User = get_user_model()

# Create superuser
if not User.objects.filter(username='admin123').exists():
    User.objects.create_superuser('admin123', 'admin@cinema.com', 'admin123')
    print("✅ Superuser created → admin123 / admin123")
else:
    print("ℹ️ Superuser already exists")

# Add movies
movies_data = [
    {"title": "Avengers: Endgame", "description": "The Avengers assemble to reverse Thanos damage.", "duration_minutes": 181, "genre": "action", "release_date": date(2019, 4, 26), "poster_url": "https://image.tmdb.org/t/p/w500/or06FN3Dka5tukK1e9sl16pB3iy.jpg", "is_active": True},
    {"title": "Inception", "description": "A thief who steals secrets through dream-sharing technology.", "duration_minutes": 148, "genre": "sci_fi", "release_date": date(2010, 7, 16), "poster_url": "https://image.tmdb.org/t/p/w500/9gk7adHYeDvHkCSEqAvQNLV5Uge.jpg", "is_active": True},
    {"title": "The Dark Knight", "description": "Batman faces the Joker who wants to plunge Gotham into anarchy.", "duration_minutes": 152, "genre": "action", "release_date": date(2008, 7, 18), "poster_url": "https://image.tmdb.org/t/p/w500/qJ2tW6WMUDux911r6m7haRef0WH.jpg", "is_active": True},
    {"title": "Interstellar", "description": "Explorers travel through a wormhole to ensure humanity survival.", "duration_minutes": 169, "genre": "sci_fi", "release_date": date(2014, 11, 7), "poster_url": "https://image.tmdb.org/t/p/w500/gEU2QniE6E77NI6lCU6MxlNBvIx.jpg", "is_active": True},
    {"title": "Spider-Man: No Way Home", "description": "Spider-Man seeks help from Doctor Strange unleashing multiverse chaos.", "duration_minutes": 148, "genre": "action", "release_date": date(2021, 12, 17), "poster_url": "https://image.tmdb.org/t/p/w500/1g0dhYtq4irTY1GPXvft6k4YLjm.jpg", "is_active": True},
    {"title": "Joker", "description": "A failed comedian turns to a life of crime in Gotham City.", "duration_minutes": 122, "genre": "drama", "release_date": date(2019, 10, 4), "poster_url": "https://image.tmdb.org/t/p/w500/udDclJoHjfjb8Ekgsd4FDteOkCU.jpg", "is_active": True},
    {"title": "The Lion King", "description": "A young lion prince learns the true meaning of responsibility.", "duration_minutes": 118, "genre": "drama", "release_date": date(2019, 7, 19), "poster_url": "https://image.tmdb.org/t/p/w500/2bXbqYdUdNVa8VIWXVfclP2ICtT.jpg", "is_active": True},
    {"title": "Doctor Strange", "description": "A surgeon discovers the hidden world of magic and alternate dimensions.", "duration_minutes": 115, "genre": "action", "release_date": date(2016, 11, 4), "poster_url": "https://m.media-amazon.com/images/M/MV5BNjgwNzAzNjk1Nl5BMl5BanBnXkFtZTgwMzQ2NjI1OTE@._V1_SX300.jpg","is_active": True},
    {"title": "The Conjuring", "description": "Paranormal investigators help a family terrorized by a dark presence.", "duration_minutes": 112, "genre": "horror", "release_date": date(2013, 7, 19), "poster_url": "https://image.tmdb.org/t/p/w500/wVYREutTvI2tmxr6ujrHT704wGF.jpg", "is_active": True},
]

for m in movies_data:
    if not Movie.objects.filter(title=m["title"]).exists():
        Movie.objects.create(**m)
        print(f"✅ Added: {m['title']}")
    else:
        print(f"ℹ️ Already exists: {m['title']}")

print("\n🎉 Done!")
print("─────────────────────────────────────")
print("👉 Go to   → http://127.0.0.1:8000/admin/")
print("👉 Username: admin123")
print("👉 Password: admin123")
print("─────────────────────────────────────")

from tickets.models import Showtime, Seat

# Auto create seats for all showtimes
for showtime in Showtime.objects.all():
    # Create seats A1-A10, B1-B10 ... J1-J10
    for row in 'ABCDEFGHIJ':
        for number in range(1, 11):
            Seat.objects.get_or_create(
                showtime=showtime,
                row=row,
                number=number,
                defaults={'is_booked': False}
            )
    print(f"✅ Seats created for: {showtime}")

print("🎉 All seats created!")