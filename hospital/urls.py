from django.urls import path
from . import views

urlpatterns = [
    path("doctor/dashboard/", views.doctor_dashboard, name="doctor_dashboard"),
    path("patient/dashboard/", views.patient_dashboard, name="patient_dashboard"),
    path("doctor/<int:doctor_id>/slots/", views.doctor_slots, name="doctor_slots"),
    path("book/<int:slot_id>/", views.book_slot, name="book_slot"),
]






