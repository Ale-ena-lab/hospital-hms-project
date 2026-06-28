# Hospital Management System

## Setup and Run

### Prerequisites

* Python 3.10 or higher
* Node.js and npm
* Serverless Framework
* Google Cloud credentials for Google Calendar integration

### Clone the Repository

```bash
git clone <repository-url>
cd hospital-hms
```

### Set Up the Django Application

Create and activate a virtual environment:

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

Install Python dependencies:

```bash
pip install -r requirements.txt
```

Navigate to the Django project directory:

```bash
cd hms
```

Run database migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

Create a superuser (optional):

```bash
python manage.py createsuperuser
```

Start the Django development server:

```bash
python manage.py runserver
```

The application will run at:

```text
http://127.0.0.1:8000/
```

### Run the Serverless Email Service

Open a new terminal.

Navigate to the email service directory:

```bash
cd email-service
```

Install Node.js dependencies:

```bash
npm install
```

Start the serverless service locally:

```bash
serverless offline
```

The email service will now listen for SIGNUP_WELCOME and BOOKING_CONFIRMATION requests from the Django application.

## System Architecture

The system is composed of two independent components: a Django web application and a serverless email microservice.

The Django application is responsible for user authentication, doctor availability management, patient booking, role-based authorization, and Google Calendar integration.

The serverless email service is responsible for sending emails such as SIGNUP_WELCOME and BOOKING_CONFIRMATION. The Django application communicates with the email service through HTTP requests whenever a user registers or successfully books an appointment.

The application uses separate models for users, availability slots, and bookings. Doctors create multiple availability slots, and patients can book available slots. A separate Booking model maintains the relationship between doctors, patients, and appointment slots.

Role-based access is enforced using custom user roles. Doctors are permitted to create and manage only their own availability slots, while patients are restricted to viewing doctors and booking available slots.

Google Calendar integration is implemented using the Google Calendar API. Once a booking is confirmed, calendar events are automatically created in both the doctor's and patient's Google Calendars using stored OAuth credentials.

## The Design Decision

A major design decision was whether to store appointment schedules directly inside the Doctor model or create a separate AvailabilitySlot model.

Option 1 was to store appointment information directly in the Doctor model. This approach would simplify the database structure initially but would make it difficult to manage multiple appointment times and bookings.

Option 2 was to create a dedicated AvailabilitySlot model linked to the doctor.

I chose the separate AvailabilitySlot model. This design keeps the database normalized, allows each doctor to create multiple slots, simplifies booking logic, and improves scalability. It also makes enforcing slot blocking easier because each slot can be individually tracked and marked as booked.

## Limitations

The current implementation is designed primarily for local development and demonstration purposes.

Google OAuth credentials are stored locally and require manual setup. Token refresh handling is limited and expired credentials may require re-authentication.

The email service runs only through serverless-offline and is not deployed to a production cloud environment.

The application currently lacks production-level features such as monitoring, centralized logging, rate limiting, and advanced security controls.

The first improvement for production would be implementing secure credential management and deploying the serverless email service to a cloud provider to ensure reliability and scalability.
