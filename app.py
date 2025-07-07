from flask import Flask, jsonify, request, render_template
from database import init_db, add_task, get_all_tasks

app = Flask(__name__)
init_db()

@app.route("/today", methods=["GET"])
def today_schedule():
    tasks = get_all_tasks()
    task_list = [{"time": t[0], "task": t[1]} for t in tasks]
    return jsonify({"tasks": task_list})

@app.route("/schedule", methods=["GET"])
def schedule_page():
    tasks = [{"time": t[0], "task": t[1]} for t in get_all_tasks()]
    return render_template("schedule.html", tasks=tasks)

@app.route("/add-task", methods=["POST"])
def add_task_route():
    data = request.json
    if not data or "time" not in data or "task" not in data:
        return jsonify({"error": "Missing 'time' or 'task'"}), 400

    add_task(data["time"], data["task"])
    return jsonify({"message": "Task added successfully"}), 201

if __name__ == "__main__":
    app.run(debug=True)