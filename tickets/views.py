from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.http import HttpResponse
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from .models import Movie, Showtime, Seat, Booking, Theatre
from .forms import RegisterForm


def home(request):
    movies = Movie.objects.filter(is_active=True)[:6]
    return render(request, 'tickets/home.html', {'movies': movies})


def movie_list(request):
    genre = request.GET.get('genre', '')
    movies = Movie.objects.filter(is_active=True)
    if genre:
        movies = movies.filter(genre=genre)
    return render(request, 'tickets/movie_list.html', {'movies': movies, 'selected_genre': genre})


def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    showtimes = Showtime.objects.filter(movie=movie).order_by('show_date', 'show_time')
    return render(request, 'tickets/movie_detail.html', {
        'movie': movie,
        'showtimes': showtimes,
    })


@login_required
def seat_selection(request, showtime_id):
    showtime = get_object_or_404(Showtime, id=showtime_id)
    seats = Seat.objects.filter(showtime=showtime).order_by('row', 'number')
    seat_map = {}
    for seat in seats:
        if seat.row not in seat_map:
            seat_map[seat.row] = []
        seat_map[seat.row].append(seat)
    return render(request, 'tickets/seat_selection.html', {
        'showtime': showtime,
        'seat_map': seat_map,
    })


@login_required
@transaction.atomic
def confirm_booking(request, showtime_id):
    if request.method != 'POST':
        return redirect('seat_selection', showtime_id=showtime_id)
    showtime = get_object_or_404(Showtime, id=showtime_id)
    seat_ids = request.POST.getlist('seats')
    if not seat_ids:
        messages.error(request, 'Please select at least one seat.')
        return redirect('seat_selection', showtime_id=showtime_id)
    seats = Seat.objects.select_for_update().filter(id__in=seat_ids, showtime=showtime)
    if seats.filter(is_booked=True).exists():
        messages.error(request, 'One or more selected seats were just booked. Please choose again.')
        return redirect('seat_selection', showtime_id=showtime_id)
    total = showtime.price * len(seat_ids)
    booking = Booking.objects.create(
        user=request.user,
        showtime=showtime,
        total_price=total,
    )
    booking.seats.set(seats)
    seats.update(is_booked=True)
    messages.success(request, 'Booking confirmed!')
    return redirect('booking_detail', booking_id=booking.id)


@login_required
def booking_detail(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    return render(request, 'tickets/booking_detail.html', {'booking': booking})


@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-booked_at')
    return render(request, 'tickets/my_bookings.html', {'bookings': bookings})


@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    if booking.status == 'cancelled':
        messages.warning(request, 'This booking is already cancelled.')
        return redirect('my_bookings')
    booking.status = 'cancelled'
    booking.save()
    booking.seats.update(is_booked=False)
    messages.success(request, 'Booking cancelled successfully.')
    return redirect('my_bookings')


@login_required
def download_ticket(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="ticket_{booking.id}.pdf"'
    doc = SimpleDocTemplate(response)
    styles = getSampleStyleSheet()
    elements = []
    elements.append(Paragraph("EliteCineBook Ticket", styles['Title']))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f"Booking ID: #{booking.id}", styles['Normal']))
    elements.append(Paragraph(f"Movie: {booking.showtime.movie.title}", styles['Normal']))
    elements.append(Paragraph(f"Theatre: {booking.showtime.theatre.name}", styles['Normal']))
    elements.append(Paragraph(f"Date: {booking.showtime.show_date}", styles['Normal']))
    elements.append(Paragraph(f"Time: {booking.showtime.show_time}", styles['Normal']))
    seats = ", ".join([str(seat) for seat in booking.seats.all()])
    elements.append(Paragraph(f"Seats: {seats}", styles['Normal']))
    elements.append(Paragraph(f"Total: Rs. {booking.total_price}", styles['Normal']))
    doc.build(elements)
    return response


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome, {user.first_name}! Your account has been created.')
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'tickets/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect(request.GET.get('next', 'home'))
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'tickets/login.html')


def logout_view(request):
    logout(request)
    return redirect('home')