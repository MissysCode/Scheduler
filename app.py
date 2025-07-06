from flask import Flask, jsonify
import json

app = Flask(__name__)

@app.route("/today")
def today_schedule():
    try:
        with open("schedule.json", "r") as file:
            schedule_data = json.load(file)
        return jsonify(schedule_data)
    except FileNotFoundError:
        return jsonify({"error": "Schedule not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)