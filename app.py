from flask import Flask, jsonify, request, render_template, redirect
from database import init_db, add_task, get_all_tasks, delete_task, assign_task_to_day
from datetime import date, timedelta

app = Flask(__name__)
init_db()

@app.route("/week", methods=["GET"])
def week_view():
    all_tasks = get_all_tasks()

    # Split tasks into unscheduled and scheduled
    unscheduled_tasks = [{"id": t[0], "task": t[1]} for t in all_tasks if t[2] is None]

    # Build a dict of day_name → list of tasks
    from datetime import datetime
    week_tasks = {day: [] for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]}

    for task in all_tasks:
        if task[2]:  # scheduled_date is not None
            day_name = datetime.fromisoformat(task[2]).strftime("%A")
            week_tasks[day_name].append({"id": task[0], "task": task[1]})

    return render_template("week.html", unscheduled=unscheduled_tasks, week_tasks=week_tasks)


@app.route("/tasks/form-add", methods=["POST"])
def add_task_form():
    task = request.form.get("task")

    if not task:
        return "Missing task", 400

    add_task(task)
    return redirect("/week")

@app.route("/tasks/delete/<task_id>", methods=["POST"])
def delete_task_route(task_id):
    delete_task(task_id)
    return redirect("/week")

# Assign a task to a day of the week (relative to today)
@app.route("/assign/<int:task_id>/<day>", methods=["POST"])
def assign_task(task_id, day):
    # Convert day name ("monday") to date
    day_names = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    today = date.today()
    today_weekday = today.weekday()  # Monday = 0
    target_weekday = day_names.index(day.lower())
    delta_days = (target_weekday - today_weekday + 7) % 7
    target_date = today + timedelta(days=delta_days)
    scheduled_date = target_date.isoformat()  # "YYYY-MM-DD"

    assign_task_to_day(task_id, scheduled_date)
    return redirect("/week")

if __name__ == "__main__":
    app.run(debug=True)