from django.db import models
import datetime
from Payment.models.customer import Customer


class Booking(models.Model):
    COURT_CHOICES = [
        ('1', 'Premium Court'),
        ('2', 'Gold Court'),
        ('3', 'Silver Court'),
    ]

    fullname = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.PositiveIntegerField(null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    court_number = models.CharField(max_length=1, choices=COURT_CHOICES)
    time = models.TimeField()
    date = models.DateField()
    playing_hours = models.CharField(max_length=50)
    status = models.BooleanField(default=False)
    booked_at = models.DateField(auto_now_add=True, blank=True, null=True)

    class Meta:
        unique_together = ['court_number', 'time', 'date']

    @staticmethod
    def get_booking_by_customer(customer_id):
        return Booking.objects.filter(customer=customer_id).booking_by('-date')

    @staticmethod
    def all_booking():
        return Booking.objects.all()

    def placeBooking(self):
        self.save()

    def __str__(self):
        return f"{self.fullname} - Court {self.court_number} - {self.time}"

    def is_valid(self, *args, **kwargs):
        now = datetime.date.today()
        if now > self.date:
            return False
        return True

    def phoneisExists(self):
        if Booking.objects.filter(phone=self.phone):
            return True
            return False

    def handlePlayingHours(self):
        try:
            hours = int(self.playing_hours)
            if hours <= 0:
                return False
            return True
        except ValueError:
            return False

    def timeisExists(self):
        if Booking.objects.filter(time=self.time):
            return True
            return False

    @staticmethod
    def get_bookings_by_customer(customer_id):
        return Booking.objects.filter(customer=customer_id)