from django.db import models
from django.utils import timezone

class Booking(models.Model):
    COURT_CHOICES = [
        (1, 'Court 1 - Premium'),
        (2, 'Court 2 - Gold'),
        (3, 'Court 3 - Silver'),
    ]

    fullname = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    court_number = models.IntegerField(choices=COURT_CHOICES)
    time_slot = models.CharField(max_length=20)
    playing_hours = models.IntegerField()
    booking_date = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('confirmed', 'Confirmed'),
            ('cancelled', 'Cancelled')
        ],
        default='pending'
    )
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        # Calculate total amount based on court type and hours
        if self.court_number == 1:  # Premium court
            base_price = 1500
        elif self.court_number == 2:  # Gold court
            base_price = 1300
        else:  # Silver court
            base_price = 1000
            
        self.total_amount = base_price * self.playing_hours
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.fullname} - Court {self.court_number} - {self.time_slot}"

    class Meta:
        ordering = ['-booking_date', 'time_slot']
        # Ensure no double bookings for same court and time slot
        unique_together = ['court_number', 'time_slot', 'booking_date'] 