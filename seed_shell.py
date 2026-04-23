from django.contrib.auth import get_user_model
from tickets.models import Movie, Theatre, Showtime, Seat
from datetime import date, time

User = get_user_model()

# ============================================
# 1. CREATE SHARED SUPERUSER (tharaka / tara123)
# ============================================
if not User.objects.filter(username='tharaka').exists():
    User.objects.create_superuser(
        username='tharaka',
        email='tharaka@cinema.com',
        password='tara123',
        role='admin'
    )
    print("✅ Shared superuser created → tharaka / tara123")
else:
    print("ℹ️ Superuser tharaka already exists")

# ============================================
# 2. CREATE THEATRES
# ============================================
theatres_data = [
    {"name": "Scope Cinemas",  "location": "Kandy, Sri Lanka",   "total_seats": 120},
    {"name": "Liberty Cinema", "location": "Negombo, Sri Lanka",  "total_seats": 80},
    {"name": "Savoy Cinema",   "location": "Colombo, Sri Lanka",  "total_seats": 100},
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

# ============================================
# 3. CREATE MOVIES
# ============================================
movies_data = [
    {"title": "Avengers: Endgame",       "description": "The Avengers assemble to reverse Thanos damage.",                        "duration_minutes": 181, "genre": "action",  "release_date": date(2019, 4, 26),  "poster_url": "https://image.tmdb.org/t/p/w500/or06FN3Dka5tukK1e9sl16pB3iy.jpg",  "is_active": True},
    {"title": "Inception",               "description": "A thief who steals secrets through dream-sharing technology.",            "duration_minutes": 148, "genre": "sci_fi",  "release_date": date(2010, 7, 16),  "poster_url": "https://image.tmdb.org/t/p/w500/9gk7adHYeDvHkCSEqAvQNLV5Uge.jpg",  "is_active": True},
    {"title": "The Dark Knight",         "description": "Batman faces the Joker who wants to plunge Gotham into anarchy.",        "duration_minutes": 152, "genre": "action",  "release_date": date(2008, 7, 18),  "poster_url": "https://image.tmdb.org/t/p/w500/qJ2tW6WMUDux911r6m7haRef0WH.jpg",  "is_active": True},
    {"title": "Interstellar",            "description": "Explorers travel through a wormhole to ensure humanity survival.",       "duration_minutes": 169, "genre": "sci_fi",  "release_date": date(2014, 11, 7),  "poster_url": "https://image.tmdb.org/t/p/w500/gEU2QniE6E77NI6lCU6MxlNBvIx.jpg",  "is_active": True},
    {"title": "Spider-Man: No Way Home", "description": "Spider-Man seeks help from Doctor Strange unleashing multiverse chaos.", "duration_minutes": 148, "genre": "action",  "release_date": date(2021, 12, 17), "poster_url": "https://image.tmdb.org/t/p/w500/1g0dhYtq4irTY1GPXvft6k4YLjm.jpg",  "is_active": True},
    {"title": "Joker",                   "description": "A failed comedian turns to a life of crime in Gotham City.",             "duration_minutes": 122, "genre": "drama",   "release_date": date(2019, 10, 4),  "poster_url": "https://image.tmdb.org/t/p/w500/udDclJoHjfjb8Ekgsd4FDteOkCU.jpg",  "is_active": True},
    {"title": "The Lion King",           "description": "A young lion prince learns the true meaning of responsibility.",         "duration_minutes": 118, "genre": "drama",   "release_date": date(2019, 7, 19),  "poster_url": "https://image.tmdb.org/t/p/w500/2bXbqYdUdNVa8VIWXVfclP2ICtT.jpg",  "is_active": True},
    {"title": "Doctor Strange",          "description": "A surgeon discovers the hidden world of magic and alternate dimensions.", "duration_minutes": 115, "genre": "action",  "release_date": date(2016, 11, 4),  "poster_url": "https://image.tmdb.org/t/p/w500/xfWac8QYDf0tRkPcTtgjaeH3A8p.jpg",  "is_active": True},
    {"title": "The Conjuring",           "description": "Paranormal investigators help a family terrorized by a dark presence.",  "duration_minutes": 112, "genre": "horror",  "release_date": date(2013, 7, 19),  "poster_url": "https://image.tmdb.org/t/p/w500/wVYREutTvI2tmxr6ujrHT704wGF.jpg",  "is_active": True},
    {"title": "Frozen II",               "description": "Elsa and Anna journey to find the origin of Elsa's powers.",            "duration_minutes": 103, "genre": "drama",   "release_date": date(2019, 11, 22), "poster_url": "https://upload.wikimedia.org/wikipedia/en/0/05/Frozen_II_%282019_film%29_poster.png", "is_active": True},
]

for m in movies_data:
    movie, created = Movie.objects.get_or_create(
        title=m["title"],
        defaults={
            "description":      m["description"],
            "duration_minutes": m["duration_minutes"],
            "genre":            m["genre"],
            "release_date":     m["release_date"],
            "poster_url":       m["poster_url"],
            "is_active":        m["is_active"],
        }
    )
    if created:
        print(f"✅ Movie added: {m['title']}")
    else:
        movie.poster_url = m["poster_url"]
        movie.save()
        print(f"ℹ️ Movie exists (poster updated): {m['title']}")

# ============================================
# 4. CREATE SHOWTIMES
# ============================================
movies_dict   = {m.title: m for m in Movie.objects.all()}
theatres_dict = {t.name:  t for t in Theatre.objects.all()}

showtimes_data = [
    {"movie": "The Conjuring",           "theatre": "Scope Cinemas",  "show_date": date(2026, 4, 24), "show_time": time(19, 0), "price": 1500.00},
    {"movie": "Avengers: Endgame",       "theatre": "Liberty Cinema", "show_date": date(2026, 4, 28), "show_time": time(15, 0), "price": 1000.00},
    {"movie": "The Dark Knight",         "theatre": "Savoy Cinema",   "show_date": date(2026, 4, 29), "show_time": time(10, 0), "price": 1500.00},
    {"movie": "Joker",                   "theatre": "Savoy Cinema",   "show_date": date(2026, 4, 30), "show_time": time(16, 0), "price": 1500.00},
    {"movie": "Doctor Strange",          "theatre": "Liberty Cinema", "show_date": date(2026, 4, 30), "show_time": time(19, 0), "price": 1000.00},
    {"movie": "Inception",               "theatre": "Savoy Cinema",   "show_date": date(2026, 5, 1),  "show_time": time(10, 0), "price": 1500.00},
    {"movie": "Inception",               "theatre": "Liberty Cinema", "show_date": date(2026, 5, 1),  "show_time": time(19, 0), "price": 1000.00},
    {"movie": "Spider-Man: No Way Home", "theatre": "Savoy Cinema",   "show_date": date(2026, 5, 1),  "show_time": time(19, 0), "price": 1500.00},
    {"movie": "The Lion King",           "theatre": "Liberty Cinema", "show_date": date(2026, 5, 3),  "show_time": time(10, 0), "price": 1000.00},
    {"movie": "Interstellar",            "theatre": "Scope Cinemas",  "show_date": date(2026, 5, 10), "show_time": time(19, 0), "price": 1500.00},
]

for s in showtimes_data:
    movie   = movies_dict.get(s["movie"])
    theatre = theatres_dict.get(s["theatre"])

    if movie and theatre:
        showtime, created = Showtime.objects.get_or_create(
            movie=movie,
            theatre=theatre,
            show_date=s["show_date"],
            show_time=s["show_time"],
            defaults={"price": s["price"]}
        )
        if created:
            print(f"✅ Showtime added: {s['movie']} @ {s['theatre']} — {s['show_date']} {s['show_time']}")
        else:
            print(f"ℹ️ Showtime exists: {s['movie']} @ {s['theatre']}")
    else:
        if not movie:
            print(f"❌ Movie not found: {s['movie']}")
        if not theatre:
            print(f"❌ Theatre not found: {s['theatre']}")

# ============================================
# 5. CREATE SEATS FOR ALL SHOWTIMES
# ============================================
for showtime in Showtime.objects.all():
    seat_count = Seat.objects.filter(showtime=showtime).count()
    if seat_count == 0:
        for row in 'ABCDEFGHIJ':
            for number in range(1, 11):
                Seat.objects.create(
                    showtime=showtime,
                    row=row,
                    number=number,
                    is_booked=False
                )
        print(f"✅ 100 seats created for: {showtime.movie.title} @ {showtime.theatre.name}")
    else:
        print(f"ℹ️ Seats exist for: {showtime.movie.title} @ {showtime.theatre.name}")

# ============================================
# 6. FINAL SUMMARY
# ============================================
print("\n" + "="*50)
print("🎉 ALL DATA LOADED SUCCESSFULLY!")
print("="*50)
print(f"👥 Users:     {User.objects.count()}")
print(f"📽️ Movies:    {Movie.objects.count()}")
print(f"🎭 Theatres:  {Theatre.objects.count()}")
print(f"🕐 Showtimes: {Showtime.objects.count()}")
print(f"💺 Seats:     {Seat.objects.count()}")
print("="*50)
print("👉 Admin panel → http://127.0.0.1:8000/admin/")
print("👉 Username: tharaka")
print("👉 Password: tara123")
print("="*50)