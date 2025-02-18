from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.views.decorators.csrf import ensure_csrf_cookie
from ..models.booking import Booking
from django.utils import timezone
from django.db import IntegrityError
from datetime import datetime

def home(request):
    return render(request, 'firsthomepage.html')

@ensure_csrf_cookie
def booking_page(request):
    return render(request, 'booking.html')

@require_http_methods(["POST"])
def create_booking(request):
    try:
        # Extract data from request
        time_str = request.POST.get('time')
        playing_hours = request.POST.get('playing_hours')
        court_type = request.POST.get('court_type')
        
        print(f"Received booking request - Time: {time_str}, Court: {court_type}, Hours: {playing_hours}")  # Debug log
        
        # Convert 12-hour time format to 24-hour format
        try:
            time_obj = datetime.strptime(time_str, '%I:%M %p')
            time = time_obj.strftime('%H:%M')
        except ValueError:
            return JsonResponse({
                'success': False,
                'error': 'Invalid time format'
            })

        # Check if slot is already booked for this specific court
        existing_booking = Booking.objects.filter(
            date=timezone.now().date(),
            time=time,
            court_number=court_type
        ).first()

        if existing_booking:
            return JsonResponse({
                'success': False,
                'error': 'This time slot is already booked for this court. Please choose another time or court.'
            })

        # Create new booking with only essential fields
        booking = Booking(
            time=time,
            date=timezone.now().date(),
            playing_hours=playing_hours,
            court_number=court_type,
            status=True  # Set initial status as confirmed
        )
        booking.save()

        return JsonResponse({
            'success': True,
            'booking_id': booking.id,
            'message': 'Booking successful!'
        })

    except IntegrityError as e:
        print(f"IntegrityError: {str(e)}")  # Debug log
        return JsonResponse({
            'success': False,
            'error': 'This time slot is already booked. Please choose another time.'
        })
    except Exception as e:
        print(f"Booking error: {str(e)}")  # Add debug logging
        return JsonResponse({
            'success': False,
            'error': str(e)
        })

@require_http_methods(["GET"])
def check_availability(request):
    try:
        date = request.GET.get('date', timezone.now().date())
        bookings = Booking.objects.filter(date=date)
        
        # Create a list of booked slots with court information
        booked_slots = [
            {
                'time': booking.time.strftime('%H:%M'),
                'court': booking.court_number,
                'status': 'booked' if booking.status else 'pending'
            }
            for booking in bookings
        ]
        
        print(f"Available slots check - Date: {date}, Booked slots: {booked_slots}")  # Debug log
        
        return JsonResponse({
            'success': True,
            'booked_slots': booked_slots
        })
    except Exception as e:
        print(f"Availability check error: {str(e)}")  # Debug log
        return JsonResponse({
            'success': False,
            'error': str(e)
        })

def booking_confirmation(request):
    try:
        latest_booking = Booking.objects.latest('booked_at')
        return render(request, 'booking_confirmation.html', {'booking': latest_booking})
    except Booking.DoesNotExist:
        return redirect('booking_page') 