from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.utils import timezone
from datetime import datetime
import requests

from .forms import AvailabilitySlotForm
from .models import AvailabilitySlot, Booking
from .google_calendar import create_calendar_event
from google_auth_oauthlib.flow import InstalledAppFlow

@login_required
def create_slot(request):
    if request.user.role != 'doctor':
        return redirect('login')

    if request.method == 'POST':
        form = AvailabilitySlotForm(request.POST)

    if form.is_valid():

        slot = form.save(commit=False)
        slot.doctor = request.user
        slot.save()

        return redirect('doctor_dashboard')

    else:

        form = AvailabilitySlotForm()

        return render(
            request,
            'appointments/create_slot.html',
            {'form': form}
        )

@login_required
def connect_google_calendar(request):

    SCOPES = [
        'https://www.googleapis.com/auth/calendar'
    ]

    flow = InstalledAppFlow.from_client_secrets_file(
        'credentials.json',
        SCOPES
    )

    creds = flow.run_local_server(port=0)

    request.user.google_token = creds.to_json()
    request.user.save()

    if request.user.role == 'doctor':
        return redirect('doctor_dashboard')

        return redirect('patient_dashboard')

@login_required
def doctor_slots(request):

    slots = AvailabilitySlot.objects.filter(
        doctor=request.user
    )

    return render(
        request,
        'appointments/doctor_slots.html',
        {'slots': slots}
    )

@login_required
def available_slots(request):
    
    if request.user.role != 'patient':
        return redirect('login')

    current_date = timezone.now().date()

    slots = AvailabilitySlot.objects.filter(
        is_booked=False,
        date__gte=current_date
    )

    return render(
        request,
        'appointments/available_slots.html',
        {'slots': slots}
    )

@login_required
@transaction.atomic
def book_slot(request, slot_id):

    if request.user.role != 'patient':
        return redirect('login')

    slot = AvailabilitySlot.objects.select_for_update().get(
        id=slot_id
    )

    if slot.is_booked:
        return render(
            request,
            'appointments/already_booked.html'
        )

    Booking.objects.create(
        patient=request.user,
        doctor=slot.doctor,
        slot=slot
    )

    slot.is_booked = True
    slot.save()

    start_datetime = datetime.combine(
        slot.date,
        slot.start_time
    )

    end_datetime = datetime.combine(
        slot.date,
        slot.end_time
    )

    # Add event to Patient Calendar
    try:
        if request.user.google_token:
            
            create_calendar_event(
                f'Appointment with Dr. {slot.doctor.username}',
                start_datetime,
                end_datetime,
                request.user.google_token
            )

    except Exception as e:
        print("Patient Calendar Error:", e)

    # Add event to Doctor Calendar
    try:
        if slot.doctor.google_token:

            create_calendar_event(
                f'Appointment with {request.user.username}',
            start_datetime,
            end_datetime,
            slot.doctor.google_token
            )

    except Exception as e:
        print("Doctor Calendar Error:", e)

    # Booking Confirmation Email
    try:
        response = requests.post(
            "http://localhost:3000/dev/send-email",
            json={
                "trigger": "BOOKING_CONFIRMATION",
            "email": request.user.email
            },
            timeout=30
        )

        print(
        "Booking Email Status:",
        response.status_code
        )

        print(
        "Booking Email Response:",
        response.text
        )

    except Exception as e:
        print("Booking Email Error:", e)

    return redirect('available_slots')

@login_required
def doctor_appointments(request):

    appointments = Booking.objects.filter(
        doctor=request.user
    )

    return render(
        request,
        'appointments/doctor_appointments.html',
        {'appointments': appointments}
    )

@login_required
def patient_appointments(request):

    appointments = Booking.objects.filter(
        patient=request.user
    )

    return render(
        request,
        'appointments/patient_appointments.html',
        {'appointments': appointments}
    )

