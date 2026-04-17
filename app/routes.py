from flask import request, render_template, redirect, url_for
from datetime import date, timedelta
from .database import add_task, delete_task, assign_task_to_day, get_tasks_for_week, find_color_by_task_name
from .services import date_for_weekday, build_week_tasks, get_task_names, pick_color_class, get_week_range


def register_routes(app):
    @app.route("/", methods=["GET"])
    def index():
        return redirect(url_for("week_view"))

    @app.route("/week", methods=["GET"])
    def week_view():

        week_start_str = request.args.get("week_start")

        if week_start_str:
            reference_date = date.fromisoformat(week_start_str)
        else:
            reference_date = date.today()

        week_start, week_end = get_week_range(reference_date)

        tasks = get_tasks_for_week(week_start.isoformat(), week_end.isoformat())

        prev_week = (week_start - timedelta(days=7)).isoformat()
        next_week = (week_start + timedelta(days=7)).isoformat()

        week_tasks = build_week_tasks(tasks)
        task_names = get_task_names(tasks)

        today = date.today()
        today_index = today.weekday()
        is_current_week = week_start <= today <= week_end

        week_range_display = f"{week_start.strftime('%b %d')} – {week_end.strftime('%b %d, %Y')}"

        return render_template(
            "week.html", 
            week_tasks=week_tasks, 
            task_names=task_names, 
            week_start=week_start.isoformat(),
            week_end=week_end.isoformat(),
            prev_week=prev_week,
            next_week=next_week,
            week_range_display=week_range_display,
            today_index=today_index,
            is_current_week=is_current_week,
        )

    @app.route("/tasks/add/<day>", methods=["POST"])
    def add_task_for_day(day):
        task = request.form.get("task", "").strip()
        week_start_str = request.form.get("week_start")

        if not task:
            return "Missing task", 400

        existing_color = find_color_by_task_name(task)

        if existing_color:
            color_class = existing_color
        else:
            color_class = pick_color_class(task)

        try:
            week_start = date.fromisoformat(week_start_str)
            scheduled_date = date_for_weekday(day, week_start)
        except ValueError:
            return f"Unknown day: {day}", 400

        add_task(task, scheduled_date, color_class)
        return redirect(url_for("week_view", week_start=week_start_str))

    @app.route("/tasks/delete/<task_id>", methods=["POST"])
    def delete_task_route(task_id):
        delete_task(task_id)
        return redirect(url_for("week_view"))

    #Route for reassigning tasks (currently unused)
    @app.route("/assign/<int:task_id>/<day>", methods=["POST"])
    def assign_task(task_id, day):
        try:
            scheduled_date = date_for_weekday(day)
        except ValueError:
            return f"Unknown day: {day}", 400

        assign_task_to_day(task_id, scheduled_date)
        return redirect(url_for("week_view"))