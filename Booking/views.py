from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.views.decorators.csrf import ensure_csrf_cookie
from .models import Booking
from django.utils import timezone
from django.db import IntegrityError

@ensure_csrf_cookie
def booking_page(request):
    return render(request, 'booking.html')

@require_http_methods(["POST"])
def create_booking(request):
    try:
        # Create new booking
        booking = Booking(
            fullname=request.POST.get('fullname'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            court_number=request.POST.get('court_number'),
            time_slot=request.POST.get('time_slot'),
            playing_hours=request.POST.get('playing_hours'),
            booking_date=timezone.now().date()
        )
        booking.save()

        # Send confirmation email
        context = {
            'booking': booking,
            'site_name': 'Dope Futsal',
        }
        
        email_html = render_to_string('email/booking_confirmation.html', context)
        email_subject = 'Booking Confirmation - Dope Futsal'
        
        try:
            send_mail(
                email_subject,
                '',  # Plain text version
                settings.DEFAULT_FROM_EMAIL,
                [booking.email],
                html_message=email_html,
                fail_silently=False,
            )
        except Exception as e:
            # Log the email error but don't fail the booking
            print(f"Email sending failed: {str(e)}")

        return JsonResponse({
            'success': True,
            'booking_id': booking.id,
            'message': 'Booking successful!'
        })

    except IntegrityError:
        return JsonResponse({
            'success': False,
            'error': 'This time slot is already booked. Please choose another time.'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })

def booking_confirmation(request):
    try:
        latest_booking = Booking.objects.latest('created_at')
        return render(request, 'booking_confirmation.html', {'booking': latest_booking})
    except Booking.DoesNotExist:
        return redirect('booking_page') 