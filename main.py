import datetime
import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/calendar"]

BASE_DIR = "/Users/anthonyjdella/Desktop/Git-Projects/airbnb-cleaning-calendar"
CREDENTIALS_PATH = os.path.join(BASE_DIR, "credentials.json")
TOKEN_PATH = os.path.join(BASE_DIR, "token.json")


def main():
    creds = None

    # Use the absolute path for token.json
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Use the absolute path for credentials.json
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_PATH, SCOPES
            )
            creds = flow.run_local_server(port=0)

        # Save the token to the absolute path
        with open(TOKEN_PATH, "w") as token:
            token.write(creds.to_json())

    try:
        service = build("calendar", "v3", credentials=creds)

        now = datetime.datetime.now().isoformat() + "Z"
        print("Getting the upcoming 14 events")
        events_result = (
            service.events()
            .list(
                calendarId="quhmbdtvkdoniffo4avofrvcugjnn546@import.calendar.google.com",
                timeMin=now,
                maxResults=14,
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
                start_date, datetime.time(13, 30))

            start_time_iso = start_time.isoformat()
            end_time_iso = end_time.isoformat()

            new_event = {
                "summary": "Focus Time",
                "location": "Rose Cliff House",
                "description": "Deep Work Session. Not Accepting Meetings.",
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
                    {"email": "anhhoang.chu@databricks.com"}
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
