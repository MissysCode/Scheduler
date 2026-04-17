from datetime import date, timedelta, datetime
import hashlib

DAY_NAMES = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
COLOR_COUNT = 7


def date_for_weekday(day: str, week_start: date) -> str:
    if day.lower() not in DAY_NAMES:
        raise ValueError("Invalid day")
    
    target_weekday = DAY_NAMES.index(day.lower())
    target_date = week_start + timedelta(days=target_weekday)
    return target_date.isoformat()

#unless given a date, this function returns the week range based on today
def get_week_range(reference_date=None):
    if reference_date is None:
        reference_date = date.today()

    start = reference_date - timedelta(days=reference_date.weekday())
    end = start + timedelta(days=6)
    return start, end

def build_week_tasks(tasks):
    week_tasks = {
        day: [] for day in DAY_NAMES
    }

    for task in tasks:
        if task.scheduled_date:
            day_name = datetime.fromisoformat(task.scheduled_date).strftime("%A").lower()
            if day_name in week_tasks:
                week_tasks[day_name].append({
                    "id": task.id,
                    "task": task.task,
                    "color_class": task.color_class,
                })

    return week_tasks

def get_task_names(tasks):
    return sorted(set(t.task for t in tasks))

def normalize_task_name(task_name):
    return task_name.strip().lower()

def pick_color_class(task_name: str) -> str:
    normalized_name = normalize_task_name(task_name)
    digest = hashlib.md5(normalized_name.encode()).hexdigest()
    color_index = int(digest, 16) % COLOR_COUNT + 1
    return f"color-{color_index}"