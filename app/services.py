from datetime import date, timedelta, datetime

DAY_NAMES = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]


def date_for_weekday(day: str) -> str:
    """
    Convert a weekday name like 'monday' to the next matching date
    (including today) as an ISO string.
    """
    today = date.today()
    today_weekday = today.weekday()
    target_weekday = DAY_NAMES.index(day.lower())
    delta_days = (target_weekday - today_weekday + 7) % 7
    target_date = today + timedelta(days=delta_days)
    return target_date.isoformat()


def build_week_tasks(all_tasks):
    week_tasks = {
        day: [] for day in
        ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    }

    for task in all_tasks:
        if task.scheduled_date:
            day_name = datetime.fromisoformat(task.scheduled_date).strftime("%A")
            if day_name in week_tasks:
                week_tasks[day_name].append({
                    "id": task.id,
                    "task": task.task,
                    "color_class": task.color_class,
                })

    return week_tasks


def get_task_names(all_tasks):
    return sorted(set(t.task for t in all_tasks))


def get_color_class(task_name, all_tasks):
    existing_names = sorted(set(t.task_name for t in all_tasks))
    name_to_color = {name: (i % 7) + 1 for i, name in enumerate(existing_names)}

    if task_name in name_to_color:
        color_index = name_to_color[task_name]
    else:
        color_index = (len(existing_names) % 7) + 1

    return f"color-{color_index}"