from django.urls import path
from . import views

urlpatterns = [

    path(
        'create-slot/',
        views.create_slot,
        name='create_slot'
    ),

    path(
        'connect-google/',
        views.connect_google_calendar,
        name='connect_google'
    ),

    path(
        'my-slots/',
        views.doctor_slots,
        name='doctor_slots'
    ),

    path(
    'available-slots/',
    views.available_slots,
    name='available_slots'
    ),

    path(
    'book-slot/<int:slot_id>/',
    views.book_slot,
    name='book_slot'
    ),

    path(
    'doctor-appointments/',
    views.doctor_appointments,
    name='doctor_appointments'
    ),

    path(
        'patient-appointments/',
        views.patient_appointments,
        name='patient_appointments'
    ),

]