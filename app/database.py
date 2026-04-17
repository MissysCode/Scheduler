import sqlite3
from flask import current_app, g
from dataclasses import dataclass

@dataclass
class Task:
    id: int
    task: str
    scheduled_date: str
    color_class: str

def init_db(app):
    with app.app_context():
        conn = get_db()
        conn.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task TEXT NOT NULL,
                scheduled_date TEXT,
                color_class TEXT
            )
        """)
        conn.commit()

def add_task(task, scheduled_date=None, color_class=None):
    conn = get_db()
    conn.execute(
        "INSERT INTO tasks (task, scheduled_date, color_class) VALUES (?, ?, ?)",
        (task, scheduled_date, color_class)
    )
    conn.commit()

def delete_task(task_id):
    conn = get_db()
    conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()

#Function for reassigning tasks (currently unused)
def assign_task_to_day(task_id, scheduled_date):
    conn = get_db()
    conn.execute(
        "UPDATE tasks SET scheduled_date = ? WHERE id = ?",
        (scheduled_date, task_id)
    )
    conn.commit()

def get_all_tasks():
    conn = get_db()
    rows = conn.execute(
        "SELECT id, task, scheduled_date, color_class FROM tasks ORDER BY scheduled_date"
    ).fetchall()
    return [Task(*row) for row in rows]

def get_tasks_for_week(start_date, end_date):
    conn = get_db()
    rows = conn.execute(
        """
        SELECT id, task, scheduled_date, color_class
        FROM tasks
        WHERE scheduled_date BETWEEN ? AND ?
        ORDER BY scheduled_date
        """,
        (start_date, end_date)
    ).fetchall()
    return [Task(*row) for row in rows]

def find_color_by_task_name(task_name):
    conn = get_db()
    row = conn.execute(
        "SELECT color_class FROM tasks WHERE LOWER(task) = ? AND color_class IS NOT NULL AND color_class != '' LIMIT 1",
        (task_name.strip().lower(),)
    ).fetchone()
    return row[0] if row else None

#Function for updating task color (currently unused)
def update_task_color(task_id, color_class):
    conn = get_db()
    conn.execute(
        "UPDATE tasks SET color_class = ? WHERE id = ?",
        (color_class, task_id)
    )
    conn.commit()

#Function for finding a missing color (currently unused)
def get_tasks_missing_colors():
    conn = get_db()
    return conn.execute(
        "SELECT id, task FROM tasks WHERE color_class IS NULL OR color_class = ''"
    ).fetchall()

def get_db():
    if "db" not in g:
        db_file = current_app.config.get("SCHEDULER_DB", "schedule.db")
        g.db = sqlite3.connect(db_file)
    return g.db

def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()