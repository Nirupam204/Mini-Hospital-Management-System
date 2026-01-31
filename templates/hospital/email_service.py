from django.core.mail import send_mail
from django.conf import settings


def send_booking_email(doctor, patient, slot, calendar_added):
    subject = "Appointment Confirmed"

    message = f"""
Appointment Details

Doctor: Dr. {doctor.username}
Patient: {patient.username}

Date: {slot.date}
Time: {slot.start_time} - {slot.end_time}

Google Calendar: {"Added" if calendar_added else "Not Added"}
"""

    recipients = []

    if doctor.email:
        recipients.append(doctor.email)
    if patient.email:
        recipients.append(patient.email)

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        recipients,
        fail_silently=True
    )


