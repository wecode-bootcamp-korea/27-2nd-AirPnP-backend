import uuid
from django.db import models

from users.models import User, Host

class Booking(models.Model): 
    booking_number = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    start_date     = models.DateTimeField()
    end_date       = models.DateTimeField()
    total_price    = models.IntegerField()
    host           = models.ForeignKey(Host, on_delete=models.CASCADE)
    user           = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at     = models.DateTimeField(auto_now_add=True)

    class Meta: 
        db_table = 'bookings'