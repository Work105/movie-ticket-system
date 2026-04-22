import os
import sys
import django

# ─── THIS MUST BE FIRST BEFORE ANY MODEL IMPORTS ───
os.environ['DJANGO_SETTINGS_MODULE'] = 'movieticket.settings'

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

django.setup()

# ─── NOW IMPORT MODELS AFTER SETUP ───
from django.contrib.auth import get_user_model
from movies.models import Movie, Showtime, Seat
from datetime import date

User = get_user_model()

print("🎬 Starting database seed...")

# ─────────────────────────────────────────
# 1. CREATE SUPERUSER
# ─────────────────────────────────────────
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser(
        username='admin',
        email='admin@cinema.com',
        password='admin123'
    )
    print("✅ Superuser created → username: admin | password: admin123")
else:
    print("ℹ️  Superuser already exists, skipping...")


# ─────────────────────────────────────────
# 2. ADD MOVIES
# ─────────────────────────────────────────
movies_data = [
    {
        "title": "Avengers: Endgame",
        "description": "The Avengers assemble once more to reverse the damage caused by Thanos.",
        "duration_minutes": 181,
        "genre": "Action",
        "release_date": date(2019, 4, 26),
        "poster_url": "https://image.tmdb.org/t/p/w500/or06FN3Dka5tukK1e9sl16pB3iy.jpg",
        "is_active": True,
    },
    {
        "title": "Inception",
        "description": "A thief who steals corporate secrets through dream-sharing technology.",
        "duration_minutes": 148,
        "genre": "Sci-Fi",
        "release_date": date(2010, 7, 16),
        "poster_url": "https://image.tmdb.org/t/p/w500/9gk7adHYeDvHkCSEqAvQNLV5Uge.jpg",
        "is_active": True,
    },
    {
        "title": "The Dark Knight",
        "description": "Batman faces the Joker, a criminal mastermind who wants to plunge Gotham into anarchy.",
        "duration_minutes": 152,
        "genre": "Action",
        "release_date": date(2008, 7, 18),
        "poster_url": "https://image.tmdb.org/t/p/w500/qJ2tW6WMUDux911r6m7haRef0WH.jpg",
        "is_active": True,
    },
    {
        "title": "Interstellar",
        "description": "A team of explorers travel through a wormhole in space to ensure humanity's survival.",
        "duration_minutes": 169,
        "genre": "Sci-Fi",
        "release_date": date(2014, 11, 7),
        "poster_url": "https://image.tmdb.org/t/p/w500/gEU2QniE6E77NI6lCU6MxlNBvIx.jpg",
        "is_active": True,
    },
    {
        "title": "Spider-Man: No Way Home",
        "description": "Spider-Man seeks help from Doctor Strange, unleashing multiverse chaos.",
        "duration_minutes": 148,
        "genre": "Action",
        "release_date": date(2021, 12, 17),
        "poster_url": "https://image.tmdb.org/t/p/w500/1g0dhYtq4irTY1GPXvft6k4YLjm.jpg",
        "is_active": True,
    },
    {
        "title": "The Lion King",
        "description": "A young lion prince flees his kingdom only to learn the true meaning of responsibility.",
        "duration_minutes": 118,
        "genre": "Animation",
        "release_date": date(2019, 7, 19),
        "poster_url": "https://image.tmdb.org/t/p/w500/2bXbqYdUdNVa8VIWXVfclP2ICtT.jpg",
        "is_active": True,
    },
    {
        "title": "Joker",
        "description": "A failed comedian turns to a life of crime and chaos in Gotham City.",
        "duration_minutes": 122,
        "genre": "Drama",
        "release_date": date(2019, 10, 4),
        "poster_url": "https://image.tmdb.org/t/p/w500/udDclJoHjfjb8Ekgsd4FDteOkCU.jpg",
        "is_active": True,
    },
    {
        "title": "Frozen II",
        "description": "Elsa and Anna embark on a journey to find the origin of Elsa's powers.",
        "duration_minutes": 103,
        "genre": "Animation",
        "release_date": date(2019, 11, 22),
        "poster_url": "https://image.tmdb.org/t/p/w500/qdfARIyszMGEKVjU4ULWL3vCiSH.jpg",
        "is_active": True,
    },
]

for movie_data in movies_data:
    if not Movie.objects.filter(title=movie_data["title"]).exists():
        Movie.objects.create(**movie_data)
        print(f"✅ Added movie: {movie_data['title']}")
    else:
        print(f"ℹ️  Already exists: {movie_data['title']}, skipping...")

print("\n🎉 Database seeding complete!")
print("─────────────────────────────────────")
print("👉 Admin login  → username: admin | password: admin123")
print("👉 Go to        → http://127.0.0.1:8000/admin")
print("─────────────────────────────────────")