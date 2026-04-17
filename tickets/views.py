

<<<<<<< HEAD
def test_view(request):
    return render(request, 'tickets/test.html')

def download_ticket(request, booking_id):
    booking = Booking.objects.get(id=booking_id)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="ticket_{booking.id}.pdf"'

    doc = SimpleDocTemplate(response)
    styles = getSampleStyleSheet()

    elements = []

    elements.append(Paragraph("🎬 EliteCineBook Ticket", styles['Title']))
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

def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    # Optional: prevent cancelling already cancelled bookings
    if booking.status == 'cancelled':
        messages.warning(request, "This booking is already cancelled.")
        return redirect('booking_confirmation', booking_id=booking.id)

    # Update status
    booking.status = 'cancelled'
    booking.save()

    messages.success(request, "Booking cancelled successfully.")
=======

# Create your views here.
>>>>>>> d38d59bcbdef07bfe51fa80f88a7b12fe87ff514
