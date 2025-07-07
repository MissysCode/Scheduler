from flask import Flask, jsonify, request, render_template, redirect
from database import init_db, add_task, get_all_tasks, delete_task

app = Flask(__name__)
init_db()

@app.route("/tasks", methods=["GET"])
def today_schedule():
    tasks = get_all_tasks()
    task_list = [{"id": t[0], "time": t[1], "task": t[2]} for t in tasks]
    return jsonify({"tasks": task_list})

@app.route("/schedule", methods=["GET"])
def schedule_page():
    tasks = [{"id": t[0], "time": t[1], "task": t[2]} for t in get_all_tasks()]
    return render_template("schedule.html", tasks=tasks)

@app.route("/tasks/form-add", methods=["POST"])
def add_task_form():
    time = request.form.get("time")
    task = request.form.get("task")

    if not time or not task:
        return "Missing time or task", 400

    add_task(time, task)
    return redirect("/schedule")

@app.route("/tasks/delete/<task_id>", methods=["POST"])
def delete_task_route(task_id):
    delete_task(task_id)
    return redirect("/schedule")

@app.route("/tasks/add", methods=["POST"])
def add_task_route():
    data = request.json
    if not data or "time" not in data or "task" not in data:
        return jsonify({"error": "Missing 'time' or 'task'"}), 400

    add_task(data["time"], data["task"])
    return jsonify({"message": "Task added successfully"}), 201

if __name__ == "__main__":
    app.run(debug=True)