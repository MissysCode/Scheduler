from flask import Flask, request, render_template, redirect
from database import init_db, add_task, get_all_tasks, delete_task, assign_task_to_day
from datetime import date, timedelta, datetime

# app = Flask(__name__, static_url_path='/scheduler/static/')
app = Flask(__name__)

init_db()

DAY_NAMES = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]


def date_for_weekday(day: str) -> str:
    """
    Convert a weekday name like 'monday' to a date (ISO string) in the current week.
    """
    today = date.today()
    today_weekday = today.weekday()  # Monday = 0
    target_weekday = DAY_NAMES.index(day.lower())
    delta_days = (target_weekday - today_weekday + 7) % 7
    target_date = today + timedelta(days=delta_days)
    return target_date.isoformat()  # "YYYY-MM-DD"


@app.route("/week", methods=["GET"])
def week_view():
    all_tasks = list(get_all_tasks())

    # Prepare empty week structure
    week_tasks = {
        day: [] for day in
        ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    }

    # Group tasks by weekday name
    for task in all_tasks:
        if task.scheduled_date:
            day_name = datetime.fromisoformat(task.scheduled_date).strftime("%A")
            if day_name in week_tasks:
                week_tasks[day_name].append({
                    "id": task.task_id,
                    "task": task.task_name,
                    "color_class": task.color_class,
                })

    # For suggestions in the "Add task" inputs
    task_names = sorted(set(t.task_name for t in all_tasks))

    return render_template("week.html", week_tasks=week_tasks, task_names=task_names)


@app.route("/tasks/add/<day>", methods=["POST"])
def add_task_for_day(day):
    """
    Add a new task and schedule it immediately on the given weekday.
    Example action URL: /tasks/add/monday
    """
    task = request.form.get("task")

    if not task:
        return "Missing task", 400

    # Determine color_class based on existing unique task names
    all_tasks = get_all_tasks()
    existing_names = sorted(set(t.task_name for t in all_tasks))
    name_to_color = {name: (i % 7) + 1 for i, name in enumerate(existing_names)}

    if task in name_to_color:
        color_index = name_to_color[task]
    else:
        color_index = (len(existing_names) % 7) + 1

    color_class = f"color-{color_index}"

    # Compute scheduled date for the given weekday
    try:
        scheduled_date = date_for_weekday(day)
    except ValueError:
        return f"Unknown day: {day}", 400

    add_task(task, scheduled_date, color_class)
    return redirect("/week")


@app.route("/tasks/delete/<task_id>", methods=["POST"])
def delete_task_route(task_id):
    delete_task(task_id)
    return redirect("/week")


# You *can* keep these if you still want:
# - /tasks/form-add (for unscheduled tasks)
# - /assign/<task_id>/<day> (reassigning)
# but your new UI won't use them anymore.

# Assign a task to a day of the week (relative to today)
@app.route("/assign/<int:task_id>/<day>", methods=["POST"])
def assign_task(task_id, day):
    scheduled_date = date_for_weekday(day)
    assign_task_to_day(task_id, scheduled_date)
    return redirect("/week")


if __name__ == "__main__":
    app.run(debug=True, port=5001)
