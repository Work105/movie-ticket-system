# 🎬 EliteCineBook — Online Movie Ticket Booking System

> A full-stack cinema ticket booking web application built with Django — supporting movie listings, interactive seat selection, user authentication, and a powerful admin panel for Elite Cinema.

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python)
![Django](https://img.shields.io/badge/Django-4.x-green?style=for-the-badge&logo=django)
![SQLite](https://img.shields.io/badge/Database-SQLite-lightgrey?style=for-the-badge&logo=sqlite)
![Bootstrap](https://img.shields.io/badge/Frontend-Bootstrap%205-purple?style=for-the-badge&logo=bootstrap)
![License](https://img.shields.io/badge/License-Educational-orange?style=for-the-badge)

---

## ✨ Features

- 🎥 Browse movies by genre — Action, Comedy, Drama, Horror, Sci-Fi, Romance, Thriller
- 🏟️ Single theatre support — Elite Cinema
- 🪑 Interactive seat selection with real-time availability
- 🗓️ Showtime scheduling per movie
- 🔐 User registration, login & logout
- 🎫 Ticket booking with confirmation
- ❌ Booking cancellation
- 📋 Booking history for each user
- 🛠️ Full Django Admin Panel for managing movies, showtimes & bookings
- 📱 Responsive frontend with Bootstrap 5

# 📁 Project Structure

```
movie-ticket-system/
│
├── accounts/                  # Custom user auth app
│   ├── migrations/
│   ├── templates/
│   ├── \_\_init\_\_.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── movie\_ticket/              # Django core project
│   ├── \_\_init\_\_.py
│   ├── admin.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── tickets/                   # Main booking app
│   ├── migrations/
│   ├── templates/
│   ├── \_\_init\_\_.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py              # Movie, Showtime, Seat, Theatre
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── templates/
│   └── base.html              # Global base template
│
├── venv/                      # Python virtual environment
├── .gitignore
├── db.sqlite3                 # SQLite database
├── manage.py
├── movies.json                # Movie fixtures
├── showtimes.json             # Showtime fixtures
├── theatres.json              # Theatre fixtures
├── seed.py                    # Database seeder script
└── README.md

---

## 🚀 Getting Started

Follow these steps carefully to run the project locally.

### Step 1 — Clone the Repository

```bash
git clone https://github.com/Work105/movie-ticket-system.git
cd movie-ticket-system
```

### Step 2 — Create \& Activate Virtual Environment

```bash
python -m venv venv
```

**Windows:**

```bash
venv\\Scripts\\activate
```

**macOS / Linux:**

```bash
source venv/bin/activate
```

### Step 3 — Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4 — Apply Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 5 — Seed the Database

```bash
python seed.py
```

This will automatically create:

* ✅ Admin superuser (`tharaka / tara123`)
* ✅ 3 Theatres (Kandy, Negombo, Colombo)
* ✅ 9 Popular movies with posters
* ✅ 10 Showtimes across theatres

> ✅ Safe to run multiple times — skips already existing records.

### Step 6 — Run the Development Server

```bash
python manage.py runserver
```

Visit the site → [http://127.0.0.1:8000](http://127.0.0.1:8000)

\---

## 🛡️ Admin Panel Setup — Step by Step

The admin panel lets you manage all movies, theatres, showtimes, seats, and users.

### Option A — Use the Seeded Admin (Recommended for Team)

After running `seed.py`, the shared admin account is already created. Skip to login.

### Option B — Create a Local Superuser Manually

If you want your own local superuser, run:

```bash
python manage.py createsuperuser
```

You will be prompted:

```
Username: your\_username
Email address: your@email.com
Password: \*\*\*\*\*\*\*\*
Password (again): \*\*\*\*\*\*\*\*
Superuser created successfully.
```

### 🔑 Log In to Admin Panel

1. Make sure the server is running:

```bash
   python manage.py runserver
   ```

2. Open your browser and go to:

```
   http://127.0.0.1:8000/admin
   ```

3. Enter your credentials:

|Field|Value|
|-|-|
|Username|`tharaka`|
|Password|`tara123`|

4. You now have full access to manage:

   * 🎬 Movies
   * 🏟️ Theatres
   * 🗓️ Showtimes
   * 🪑 Seats
   * 👥 Users \& Bookings

> ⚠️ \*\*Team Note:\*\* All teammates use the shared account `tharaka / tara123`. Do \*\*not\*\* change this password without notifying the team.



## 👥 Team

236007G as Work105
236046A as wtharakaherath-ux
236071U as wimalsha1015-arch

🔗 GitHub Repository → [https://github.com/Work105/movie-ticket-system](https://github.com/Work105/movie-ticket-system)

\---

## 📄 License

This project is for **educational purposes** only.
