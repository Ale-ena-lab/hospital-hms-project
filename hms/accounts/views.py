from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegisterForm

import requests
def signup(request):

    if request.method == 'POST':

        form = UserRegisterForm(request.POST)

        if form.is_valid():
            user = form.save()

            try:
                response = requests.post(
                    "http://localhost:3000/dev/send-email",
                    json={
                        "trigger": "SIGNUP_WELCOME",
                        "email": user.email
                    },
                    timeout=30
                )

                print("Email Status:", response.status_code)
                print("Email Response:", response.text)

            except Exception as e:
                print("Email Error:", e)

            login(request, user)

            if user.role == 'doctor':
                return redirect('doctor_dashboard')
            else:
                return redirect('patient_dashboard')

    else:
        form = UserRegisterForm()

    return render(request, 'accounts/signup.html', {'form': form})
def user_login(request):

    if request.method == 'POST':

        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():

            user = form.get_user()

            login(request, user)

            if user.role == 'doctor':
                return redirect('doctor_dashboard')
            else:
                return redirect('patient_dashboard')

    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')

def doctor_dashboard(request):
    return render(
        request,
        'accounts/doctor_dashboard.html'
    )


def patient_dashboard(request):
    return render(
        request,
        'accounts/patient_dashboard.html'
    )