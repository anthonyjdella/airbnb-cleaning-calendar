import os
import datetime
import subprocess

LAST_RUN_FILE = "/Users/anthonyjdella/Desktop/Git-Projects/airbnb-cleaning-calendar/last_run.txt"
SCRIPT_PATH = "/Users/anthonyjdella/Desktop/Git-Projects/airbnb-cleaning-calendar/main.py"
LOG_FILE = "/Users/anthonyjdella/Desktop/Git-Projects/airbnb-cleaning-calendar/test_cron.log"


def main():
    now = datetime.datetime.now()
    last_run = None

    # Read the last run date
    if os.path.exists(LAST_RUN_FILE):
        with open(LAST_RUN_FILE, "r") as file:
            last_run_str = file.read().strip()
            last_run = datetime.datetime.fromisoformat(last_run_str)

    # Check if 14 days have passed
    if last_run is None or (now - last_run).days >= 14:
        # Update the last run file
        with open(LAST_RUN_FILE, "w") as file:
            file.write(now.isoformat())

        # Run the main script
        subprocess.run([
            "/Users/anthonyjdella/.pyenv/shims/python3", SCRIPT_PATH
        ], stdout=open(LOG_FILE, "a"), stderr=subprocess.STDOUT)


if __name__ == "__main__":
    main()
