from datetime import datetime, date
import json

# Example tasks
tasks = [
    {"time": "08:00", "task": "Morning walk"},
    {"time": "09:00", "task": "Coding session"},
    {"time": "12:00", "task": "Lunch break"},
    {"time": "14:00", "task": "Grocery shopping"},
]

def get_today_schedule():
    today = datetime.now().strftime("%A, %B, %d, %Y")
    print(f"Today's schedule for {today} :\n")
    for task in tasks:
        print(task)

# JSON data
schedule_data = {
    "date": str(date.today()),
    "tasks": tasks
}

# Save to schedule.json
with open("schedule.json", "w") as json_file:
    json.dump(schedule_data, json_file, indent=4)

print("Schedule saved to schedule.json")

if __name__ == "__main__":
    get_today_schedule()