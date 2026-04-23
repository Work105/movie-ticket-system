import os
import sys
import django

# ─── THIS MUST BE FIRST BEFORE ANY MODEL IMPORTS ───
os.environ['DJANGO_SETTINGS_MODULE'] = 'movie_ticket.settings'

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

django.setup()

# ─── NOW IMPORT MODELS AFTER SETUP ───
from django.contrib.auth import get_user_model
from tickets.models import Movie, Showtime, Seat, Theatre
from datetime import date

User = get_user_model()

print("🎬 Starting database seed...")

# ─────────────────────────────────────────
# 1. CREATE SHARED SUPERUSER (tharaka / tara123)
# ─────────────────────────────────────────
if not User.objects.filter(username='tharaka').exists():
    User.objects.create_superuser(
        username='tharaka',
        email='tharaka@cinema.com',
        password='tara123',
        role='admin'
    )
    print("✅ Shared superuser created → tharaka / tara123")
else:
    print("ℹ️  Superuser tharaka already exists")

# ─────────────────────────────────────────
# 2. CREATE THEATRES
# ─────────────────────────────────────────
theatres_data = [
    {"name": "Scope Cinemas", "location": "Kandy, Sri Lanka", "total_seats": 120},
    {"name": "Liberty Cinema", "location": "Negombo, Sri Lanka", "total_seats": 80},
    {"name": "Savoy Cinema", "location": "Colombo, Sri Lanka", "total_seats": 100},
]

for t in theatres_data:
    theatre, created = Theatre.objects.get_or_create(
        name=t["name"],
        defaults={"location": t["location"], "total_seats": t["total_seats"]}
    )
    if created:
        print(f"✅ Theatre added: {t['name']}")
    else:
        print(f"ℹ️ Theatre already exists: {t['name']}")

# ─────────────────────────────────────────
# 3. ADD MOVIES
# ─────────────────────────────────────────
movies_data = [
    {
        "title": "Avengers: Endgame",
        "description": "The Avengers assemble once more to reverse the damage caused by Thanos.",
        "duration_minutes": 181,
        "genre": "action",
        "release_date": date(2019, 4, 26),
        "poster_url": "https://image.tmdb.org/t/p/w500/or06FN3Dka5tukK1e9sl16pB3iy.jpg",
        "is_active": True,
    },
    {
        "title": "Inception",
        "description": "A thief who steals corporate secrets through dream-sharing technology.",
        "duration_minutes": 148,
        "genre": "sci_fi",
        "release_date": date(2010, 7, 16),
        "poster_url": "https://image.tmdb.org/t/p/w500/9gk7adHYeDvHkCSEqAvQNLV5Uge.jpg",
        "is_active": True,
    },
    {
        "title": "The Dark Knight",
        "description": "Batman faces the Joker, a criminal mastermind who wants to plunge Gotham into anarchy.",
        "duration_minutes": 152,
        "genre": "action",
        "release_date": date(2008, 7, 18),
        "poster_url": "https://image.tmdb.org/t/p/w500/qJ2tW6WMUDux911r6m7haRef0WH.jpg",
        "is_active": True,
    },
    {
        "title": "Interstellar",
        "description": "A team of explorers travel through a wormhole in space to ensure humanity's survival.",
        "duration_minutes": 169,
        "genre": "sci_fi",
        "release_date": date(2014, 11, 7),
        "poster_url": "https://image.tmdb.org/t/p/w500/gEU2QniE6E77NI6lCU6MxlNBvIx.jpg",
        "is_active": True,
    },
    {
        "title": "Spider-Man: No Way Home",
        "description": "Spider-Man seeks help from Doctor Strange, unleashing multiverse chaos.",
        "duration_minutes": 148,
        "genre": "action",
        "release_date": date(2021, 12, 17),
        "poster_url": "https://image.tmdb.org/t/p/w500/1g0dhYtq4irTY1GPXvft6k4YLjm.jpg",
        "is_active": True,
    },
    {
        "title": "The Lion King",
        "description": "A young lion prince flees his kingdom only to learn the true meaning of responsibility.",
        "duration_minutes": 118,
        "genre": "drama",
        "release_date": date(2019, 7, 19),
        "poster_url": "https://image.tmdb.org/t/p/w500/2bXbqYdUdNVa8VIWXVfclP2ICtT.jpg",
        "is_active": True,
    },
    {
        "title": "Joker",
        "description": "A failed comedian turns to a life of crime and chaos in Gotham City.",
        "duration_minutes": 122,
        "genre": "drama",
        "release_date": date(2019, 10, 4),
        "poster_url": "https://image.tmdb.org/t/p/w500/udDclJoHjfjb8Ekgsd4FDteOkCU.jpg",
        "is_active": True,
    },
    {
        "title": "Doctor Strange",
        "description": "A surgeon discovers the hidden world of magic and alternate dimensions.",
        "duration_minutes": 115,
        "genre": "action",
        "release_date": date(2016, 11, 4),
        "poster_url": "https://image.tmdb.org/t/p/w500/xfWac8QYDf0tRkPcTtgjaeH3A8p.jpg",
        "is_active": True,
    },
    {
        "title": "The Conjuring",
        "description": "Paranormal investigators help a family terrorized by a dark presence.",
        "duration_minutes": 112,
        "genre": "horror",
        "release_date": date(2013, 7, 19),
        "poster_url": "https://image.tmdb.org/t/p/w500/wVYREutTvI2tmxr6ujrHT704wGF.jpg",
        "is_active": True,
    },
]

for movie_data in movies_data:
    if not Movie.objects.filter(title=movie_data["title"]).exists():
        Movie.objects.create(**movie_data)
        print(f"✅ Added movie: {movie_data['title']}")
    else:
        print(f"ℹ️  Already exists: {movie_data['title']}, skipping...")

# ─────────────────────────────────────────
# 4. CREATE SHOWTIMES
# ─────────────────────────────────────────
movies_dict = {m.title: m for m in Movie.objects.all()}
theatres_dict = {t.name: t for t in Theatre.objects.all()}

showtimes_data = [
    {"movie": "The Conjuring", "theatre": "Scope Cinemas", "show_date": date(2026, 4, 24), "show_time": "19:00:00", "price": 1500.00},
    {"movie": "Inception", "theatre": "Scope Cinemas", "show_date": date(2026, 5, 1), "show_time": "10:00:00", "price": 1500.00},
    {"movie": "Spider-Man: No Way Home", "theatre": "Scope Cinemas", "show_date": date(2026, 5, 1), "show_time": "10:00:00", "price": 1500.00},
    {"movie": "Interstellar", "theatre": "Scope Cinemas", "show_date": date(2026, 5, 10), "show_time": "19:00:00", "price": 1500.00},
    {"movie": "Avengers: Endgame", "theatre": "Liberty Cinema", "show_date": date(2026, 4, 28), "show_time": "15:00:00", "price": 1000.00},
    {"movie": "Doctor Strange", "theatre": "Liberty Cinema", "show_date": date(2026, 4, 30), "show_time": "19:00:00", "price": 1000.00},
    {"movie": "The Lion King", "theatre": "Liberty Cinema", "show_date": date(2026, 5, 3), "show_time": "10:00:00", "price": 1000.00},
    {"movie": "Inception", "theatre": "Liberty Cinema", "show_date": date(2026, 5, 1), "show_time": "19:00:00", "price": 1000.00},
    {"movie": "The Dark Knight", "theatre": "Savoy Cinema", "show_date": date(2026, 4, 29), "show_time": "10:00:00", "price": 1500.00},
    {"movie": "Joker", "theatre": "Savoy Cinema", "show_date": date(2026, 4, 30), "show_time": "16:00:00", "price": 1500.00},
]

from datetime import time

for s in showtimes_data:
    movie = movies_dict.get(s["movie"])
    theatre = theatres_dict.get(s["theatre"])
    
    if movie and theatre:
        showtime, created = Showtime.objects.get_or_create(
            movie=movie,
            theatre=theatre,
            show_date=s["show_date"],
            show_time=time.fromisoformat(s["show_time"]),
            defaults={"price": s["price"]}
        )
        if created:
            print(f"✅ Showtime added: {s['movie']} at {s['theatre']} on {s['show_date']}")
        else:
            print(f"ℹ️ Showtime already exists: {s['movie']} at {s['theatre']}")

print("\n🎉 Database seeding complete!")
print("─────────────────────────────────────")
print("👉 Admin login  → username: tharaka | password: tara123")
print("👉 Go to        → http://127.0.0.1:8000/admin")
print("─────────────────────────────────────")