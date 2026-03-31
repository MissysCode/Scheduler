from flask import request, render_template, redirect, url_for
from .database import add_task, get_all_tasks, delete_task, assign_task_to_day
from .services import date_for_weekday, build_week_tasks, get_task_names, get_color_class


def register_routes(app):
    @app.route("/", methods=["GET"])
    def index():
        return redirect(url_for("week_view"))

    @app.route("/week", methods=["GET"])
    def week_view():
        all_tasks = list(get_all_tasks())
        week_tasks = build_week_tasks(all_tasks)
        task_names = get_task_names(all_tasks)
        return render_template("week.html", week_tasks=week_tasks, task_names=task_names)

    @app.route("/tasks/add/<day>", methods=["POST"])
    def add_task_for_day(day):
        task = request.form.get("task", "").strip()

        if not task:
            return "Missing task", 400

        all_tasks = list(get_all_tasks())
        color_class = get_color_class(task, all_tasks)

        try:
            scheduled_date = date_for_weekday(day)
        except ValueError:
            return f"Unknown day: {day}", 400

        add_task(task, scheduled_date, color_class)
        return redirect(url_for("week_view"))

    @app.route("/tasks/delete/<task_id>", methods=["POST"])
    def delete_task_route(task_id):
        delete_task(task_id)
        return redirect(url_for("week_view"))

    @app.route("/assign/<int:task_id>/<day>", methods=["POST"])
    def assign_task(task_id, day):
        try:
            scheduled_date = date_for_weekday(day)
        except ValueError:
            return f"Unknown day: {day}", 400

        assign_task_to_day(task_id, scheduled_date)
        return redirect(url_for("week_view"))