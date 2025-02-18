from django.contrib import admin
from django.urls import path
from .views.tregistration import Tregistration
from .views.booking import Booking, FutsalBooking, add_booking, delete_booking, update_booking, sendfutsalmail
from .views.futsalbooking import futsalbooking
from Payment.middlewares.auth import auth_middleware
from .views.all_bookings import all_booking
from .views.report import showreport
from .views.booking_views import booking_page, create_booking, booking_confirmation, home

urlpatterns = [
    path('', home, name='home'),
    path('Tregistration', auth_middleware(Tregistration.as_view()), name='Tregistration'),
    path('futsalbooking_form/', booking_page, name='booking_page'),
    path('book/', create_booking, name='create_booking'),
    path('booking-confirmation/', booking_confirmation, name='booking_confirmation'),
    path('bookings', auth_middleware(all_booking.as_view()), name='bookings'),
    path('update_booking/<int:id>', update_booking, name='update-booking'),
    path('add_booking', auth_middleware(add_booking), name='add-booking'),
    path('delete_booking/<int:id>', delete_booking, name='delete-booking'),
    path('futsal_booking', auth_middleware(futsalbooking.as_view()), name='futsal-booking'),
    path('sendmail', sendfutsalmail, name='send-mail'),
    path('report', auth_middleware(showreport), name='report')
]
