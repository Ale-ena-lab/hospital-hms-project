import json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build


def create_calendar_event(summary, start_time, end_time, user_token):
    creds = Credentials.from_authorized_user_info(
        json.loads(user_token)
    )

    service = build(
        'calendar',
        'v3',
        credentials=creds
    )

    event = {
        'summary': summary,
        'start': {
            'dateTime': start_time.isoformat(),
            'timeZone': 'Asia/Kolkata',
        },
        'end': {
            'dateTime': end_time.isoformat(),
            'timeZone': 'Asia/Kolkata',
        },
    }

    service.events().insert(
        calendarId='primary',
        body=event
    ).execute()