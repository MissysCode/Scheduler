from datetime import datetime, date
import json
import os

SCHEDULE_FILE = "schedule.json"

# Get today's schedule
def get_today_schedule():
    schedule = load_schedule()
    today = datetime.now().strftime("%A, %B %d %Y")
    print(f"Today's schedule for {today} :\n")
    for task in schedule.get("tasks", []):
        print(f"{task['time']} - {task['task']}")

if __name__ == "__main__":
    get_today_schedule()