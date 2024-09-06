import datetime
import os
import json

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/calendar"]


def get_credentials():
    creds_info = json.loads(os.getenv('GOOGLE_CREDENTIALS'))
    print(creds_info)
    creds = Credentials.from_service_account_info(creds_info, scopes=SCOPES)
    return creds


def main():
    creds = get_credentials()

    try:
        service = build("calendar", "v3", credentials=creds)

        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        print("Getting the upcoming 10 events")
        events_result = (
            service.events()
            .list(
                calendarId="quhmbdtvkdoniffo4avofrvcugjnn546@import.calendar.google.com",
                timeMin=now,
                maxResults=10,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        events = events_result.get("items", [])

        if not events:
            print("No upcoming events found.")
            return

        for event in events:
            start = event["start"].get("dateTime", event["start"].get("date"))
            end = event["end"].get("dateTime", event["end"].get("date"))
            print(
                f"Event starts at {start}, ends at {end}, summary: {event.get('summary')}")

            start_date = datetime.datetime.fromisoformat(start).date()

            # Check if a cleaning event already exists for the same day
            existing_cleaning_events = (
                service.events()
                .list(
                    calendarId="primary",
                    timeMin=start_date.isoformat() + "T00:00:00Z",
                    timeMax=start_date.isoformat() + "T23:59:59Z",
                    singleEvents=True,
                    q="Cleaning Time",  # Query event by summary
                )
                .execute()
            )

            if existing_cleaning_events.get("items"):
                print(
                    f"A cleaning event already exists for {start_date}. Skipping creation.")
                continue

            # Create a new event from 11:00 AM to 4:00 PM
            start_time = datetime.datetime.combine(
                start_date, datetime.time(11, 0))
            end_time = datetime.datetime.combine(
                start_date, datetime.time(16, 0))

            start_time_iso = start_time.isoformat()
            end_time_iso = end_time.isoformat()

            new_event = {
                "summary": "Cleaning Time",
                "location": "Rose Cliff House",
                "description": "Guest is leaving, time to clean.",
                "colorId": 6,
                "start": {
                    "dateTime": start_time_iso,
                    "timeZone": "America/Los_Angeles"
                },
                "end": {
                    "dateTime": end_time_iso,
                    "timeZone": "America/Los_Angeles"
                },
                "attendees": [
                    {"email": "leeznon@gmail.com"},
                    {"email": "rosecliffhouse@gmail.com"}
                ],
                "reminders": {
                    "useDefault": False,
                    "overrides": [
                        {"method": "popup", "minutes": 30},
                        {"method": "popup", "minutes": 0},
                    ]
                }
            }

            created_event = service.events().insert(
                calendarId="primary", body=new_event
            ).execute()

            print(f"Event created: {created_event.get('htmlLink')}")

    except HttpError as error:
        print(f"An error occurred: {error}")


if __name__ == "__main__":
    main()
