from flask import Flask, request, render_template, redirect
from database import init_db, add_task, get_all_tasks, delete_task, assign_task_to_day
from datetime import date, timedelta, datetime

app = Flask(__name__)
init_db()

@app.route("/week", methods=["GET"])
def week_view():   
    all_tasks = list(get_all_tasks())

    # Split tasks into unscheduled and scheduled
    unscheduled_tasks = [
        {"id": t.task_id, "task": t.task_name, "color_class": t.color_class}
        for t in all_tasks if t.scheduled_date is None
    ]

    # Prepare empty week structure
    week_tasks = {day: [] for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]}

    for task in all_tasks:
        if task.scheduled_date:
            day_name = datetime.fromisoformat(task.scheduled_date).strftime("%A")
            if day_name in week_tasks:
                week_tasks[day_name].append({
                    "id": task.task_id,
                    "task": task.task_name,
                    "color_class": task.color_class
                })

    return render_template("week.html", unscheduled=unscheduled_tasks, week_tasks=week_tasks)


@app.route("/tasks/form-add", methods=["POST"])
def add_task_form():
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

    add_task(task, None, color_class)
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

    print(f"[DEBUG] Received day: {day}")
 
    today = date.today()
    today_weekday = today.weekday()  # Monday = 0
    target_weekday = day_names.index(day.lower())
    delta_days = (target_weekday - today_weekday + 7) % 7
    target_date = today + timedelta(days=delta_days)
    scheduled_date = target_date.isoformat()  # "YYYY-MM-DD"

    print(f"[DEBUG] Received day: {scheduled_date}")

    assign_task_to_day(task_id, scheduled_date)
    return redirect("/week")

if __name__ == "__main__":
    app.run(debug=True, port=5001)
