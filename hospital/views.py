from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from accounts.models import User
from .models import Slot
from .google_calendar import create_calendar_event
from .email_service import send_booking_email



def doctor_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_doctor():
            return HttpResponseForbidden("Doctor access only")
        return view_func(request, *args, **kwargs)
    return wrapper


def patient_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_patient():
            return HttpResponseForbidden("Patient access only")
        return view_func(request, *args, **kwargs)
    return wrapper

@doctor_required
def doctor_dashboard(request):
    if request.method == "POST":
        Slot.objects.create(
            doctor=request.user,
            date=request.POST["date"],
            start_time=request.POST["start_time"],
            end_time=request.POST["end_time"],
        )
        return redirect("doctor_dashboard")

    slots = Slot.objects.filter(doctor=request.user)
    bookings = Slot.objects.filter(doctor=request.user, is_booked=True)

    return render(request, "hospital/doctor_dashboard.html", {
        "slots": slots,
        "bookings": bookings
    })


@patient_required
def patient_dashboard(request):
    doctors = User.objects.filter(role=User.DOCTOR)
    bookings = Slot.objects.filter(patient=request.user)

    return render(request, "hospital/patient_dashboard.html", {
        "doctors": doctors,
        "bookings": bookings
    })


@patient_required
def doctor_slots(request, doctor_id):
    doctor = get_object_or_404(User, id=doctor_id, role=User.DOCTOR)
    slots = Slot.objects.filter(doctor=doctor, is_booked=False)

    return render(request, "hospital/doctor_slots.html", {
        "doctor": doctor,
        "slots": slots
    })


@patient_required
def book_slot(request, slot_id):
   @patient_required
def book_slot(request, slot_id):
    slot = get_object_or_404(Slot, id=slot_id, is_booked=False)

    slot.is_booked = True
    slot.patient = request.user
    slot.save()

    calendar_added = False

    if slot.doctor.google_access_token:
        event_id = create_calendar_event(slot.doctor, slot)
        if event_id:
            calendar_added = True

    send_booking_email(
        doctor=slot.doctor,
        patient=slot.patient,
        slot=slot,
        calendar_added=calendar_added
    )

    return redirect("patient_dashboard")

