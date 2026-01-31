import os
from datetime import datetime
from zoneinfo import ZoneInfo

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request


def _get_credentials_for_user(user):
    if not user.google_access_token:
        return None

    client_id = os.environ.get("GOOGLE_CLIENT_ID")
    client_secret = os.environ.get("GOOGLE_CLIENT_SECRET")

    if not client_id or not client_secret:
        return None

    creds = Credentials(
        token=user.google_access_token,
        refresh_token=user.google_refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=client_id,
        client_secret=client_secret,
        scopes=["https://www.googleapis.com/auth/calendar"],
    )

    if creds.expired and creds.refresh_token:
        try:
            creds.refresh(Request())
            user.google_access_token = creds.token
            if creds.refresh_token:
                user.google_refresh_token = creds.refresh_token
            user.google_token_expiry = creds.expiry
            user.save(update_fields=[
                "google_access_token",
                "google_refresh_token",
                "google_token_expiry",
            ])
        except Exception:
            return None

    return creds


def create_calendar_event(doctor, slot):
    creds = _get_credentials_for_user(doctor)
    if not creds:
        return None

    service = build("calendar", "v3", credentials=creds)

    tz = ZoneInfo("Asia/Kolkata")
    start_dt = datetime.combine(slot.date, slot.start_time).replace(tzinfo=tz)
    end_dt = datetime.combine(slot.date, slot.end_time).replace(tzinfo=tz)

    event = {
        "summary": f"Appointment with {slot.patient.username}",
        "description": "Booked via Hospital Management System",
        "start": {"dateTime": start_dt.isoformat(), "timeZone": "Asia/Kolkata"},
        "end": {"dateTime": end_dt.isoformat(), "timeZone": "Asia/Kolkata"},
    }

    created_event = service.events().insert(
        calendarId="primary",
        body=event
    ).execute()

    return created_event.get("id")
