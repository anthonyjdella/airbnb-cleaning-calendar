# Airbnb Cleaning Calendar

This cron job automatically blocks cleaning time on your calendar every 14 days when a guest checks out. This ensures your calendar remains clear and you stay on top of cleaning schedules.

## Usage

This makes use of the Google Calendar API and the exported Airbnb calendar bookings.

The cron job runs every 14 days at 12:16 PM local time. If it has run within the last 14 days, it won't execute again. After 14 days, it will update the next 14 Airbnb events and block time on your calendar.

### Editing the Cron Job

To edit the cron job, use the following command:

```bash
crontab -e
```

```bash
16 12 * * * /Users/anthonyjdella/.pyenv/shims/python3 /Users/anthonyjdella/Desktop/Git-Projects/airbnb-cleaning-calendar/check_and_run.py >> /Users/anthonyjdella/Desktop/Git-Projects/airbnb-cleaning-calendar/test_cron.log 2>&1
```

To view the cron job, use the following command:

```bash
crontab -l
```
