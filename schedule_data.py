from datetime import date
import os
import json

SCHEDULE_FILE = "schedule.json"

# Load schedule from file or create a new one    
def load_schedule():
    if os.path.exists(SCHEDULE_FILE):
        try:
            with open(SCHEDULE_FILE, "r") as json_file:
                return json.load(json_file)
        except json.JSONDecodeError:
            print("⚠️  Warning: schedule.json is empty or invalid. Creating a new schedule.")
            return {"date": str(date.today()), "tasks": []}
    else:
        return {"date": str(date.today()), "tasks": []}

# Save schedule to file
def save_schedule(schedule_data):
    with open(SCHEDULE_FILE, "w") as json_file:
        json.dump(schedule_data, json_file, indent=4)
        print("Schedule saved to schedule.json")

# Add a task
def add_task(time, task_name):
    schedule = load_schedule()
    schedule["tasks"].append({"time": time, "task": task_name})
    save_schedule(schedule)
    print(f"Added task: {time} - {task_name}")
    return schedule