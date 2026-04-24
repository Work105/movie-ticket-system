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
- 📱 Responsive frontend with Bootstrap 

 ## 🛠️ Tech Stack

| Layer       | Technology                       |
|-------------|----------------------------------|
| Backend     | Django 4.x (Python 3.10+)       |
| Database    | SQLite3 (`db.sqlite3`)           |
| Frontend    | HTML5, CSS3, Bootstrap           |
| Auth System | Django Auth + Custom User Model  |
| Admin Panel | Django Admin (`/admin`)          |
| Data Load   | Django Fixtures (JSON files)     |
| Environment | Python virtualenv (`venv/`)      |


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
├── seats.json                   # Seats fixtures
└── README.md

---

## 🚀 Getting Started

Follow these steps **carefully** to run the project on your local machine.

### Step 1 — Clone the Repository

```bash
git clone https://github.com/Work105/movie-ticket-system.git
cd movie-ticket-system
```

### Step 2 — Create & Activate Virtual Environment

```bash
python -m venv venv
```

**Windows:**
```bash
venv\Scripts\activate
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

### Step 5 — Load Fixture Data

Load theatres, movies, and showtimes from the JSON fixture files:

```bash
python manage.py loaddata theatres.json
python manage.py loaddata movies.json
python manage.py loaddata showtimes.json
python manage.py loaddata seats.json
```

> ✅ This loads all pre-built data instantly without any seed script.

### Step 6 — Create Your Own Admin Superuser

> ⚠️ **Important:** Every teammate must create their own superuser locally.
> This is because `db.sqlite3` is a **local file** — it is not shared between machines.
> You cannot reuse another person's superuser on your device.

```bash
python manage.py createsuperuser
```

You will be prompted to enter:

```
Username: choose_any_username
Email address: your@email.com
Password: ********
Password (again): ********
Superuser created successfully.
```

> 💡 Pick any username and password you like — it only exists on **your machine**.

### Step 7 — Run the Development Server

```bash
python manage.py runserver
```

Visit the site → [http://127.0.0.1:8000](http://127.0.0.1:8000)

\---

## 🛡️ Admin Panel — Step by Step Login Guide

The admin panel gives you full control over movies, theatres, showtimes, seats, and users.

**Step 1** — Start the server:
```bash
python manage.py runserver
```

**Step 2** — Open this URL in your browser:
```
http://127.0.0.1:8000/admin
```

**Step 3** — Log in with the superuser credentials **you created** in Step 6 above.

**Step 4** — You now have full access to manage:

| Section      | What You Can Do                        |
|--------------|----------------------------------------|
| 🎬 Movies     | Add, edit, delete movies              |
| 🏟️ Theatres   | Add, edit, delete theatres            |
| 🗓️ Showtimes  | Schedule movie showtimes per theatre  |
| 🪑 Seats      | Manage seat availability              |
| 👥 Users      | View registered users and bookings    |

---

## ❓ Why No `seed.py`?

The project previously used a `seed.py` script that tried to create a shared superuser. This caused problems because **`db.sqlite3` is a local file** — it is not shared between devices. Every teammate had a separate database, so the shared superuser credentials didn't work across machines, and running the script twice caused conflicts.

**The fix:** Each teammate creates their own superuser locally with `python manage.py createsuperuser`. Movie, theatre, and showtime data is loaded cleanly from JSON fixture files instead.



## 👥 Team

236007G as Work105
236046A as wtharakaherath-ux
236071U as wimalsha1015-arch

🔗 GitHub Repository → [https://github.com/Work105/movie-ticket-system](https://github.com/Work105/movie-ticket-system)

\---

## 📄 License

This project is for **educational purposes** only.
