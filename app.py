from flask import Flask, jsonify, request
from schedule_data import load_schedule, add_task

app = Flask(__name__)

@app.route("/today", methods=["GET"])
def today_schedule():
    schedule = load_schedule()
    return jsonify(schedule)



@app.route("/add-task", methods=["POST"])
def add_task_route():
    data = request.json
    if not data or "time" not in data or "task" not in data:
        return jsonify({"error": "Missing 'time' or 'task' in request"}), 400
    
    updated_schedule = add_task(data["time"], data["task"])
    return jsonify(updated_schedule), 201

if __name__ == "__main__":
    app.run(debug=True)