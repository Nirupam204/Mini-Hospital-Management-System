from django.db import models
from accounts.models import User


class Slot(models.Model):
    doctor = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="doctor_slots"
    )
    patient = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True
    )
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_booked = models.BooleanField(default=False)
    google_event_id = models.CharField(max_length=255, null=True, blank=True)


    def __str__(self):
        return f"{self.doctor.username} | {self.date} {self.start_time}-{self.end_time}"





