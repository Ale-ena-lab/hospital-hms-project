import json
import smtplib
from email.mime.text import MIMEText


def send_email(event, context):

    body = json.loads(event['body'])

    trigger = body.get('trigger')
    email = body.get('email')

    if trigger == 'SIGNUP_WELCOME':

        subject = 'Welcome to HMS'

        message = '''
Welcome to Hospital Management System.

Thank you for registering.
'''

    elif trigger == 'BOOKING_CONFIRMATION':

        subject = 'Appointment Confirmed'

        message = '''
Your appointment has been confirmed.
'''

    else:
        subject = 'Notification'
        message = 'Hospital notification.'

    msg = MIMEText(message)

    msg['Subject'] = subject
    msg['From'] = 'aleenabiju1104@gmail.com'
    msg['To'] = email

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()

    server.login(
        'aleenabiju1104@gmail.com',
        'qvml ouak sduf kvex'
    )

    server.send_message(msg)
    server.quit()

    return {
        'statusCode': 200,
        'body': json.dumps(
            {'message': 'Email sent successfully'}
        )
    }