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
                scheduled_date TEXT
            )
        """)
        # Check if 'color_class' column exists
        columns = [col[1] for col in conn.execute("PRAGMA table_info(tasks)").fetchall()]

        # If you add new fields, you can copy the following code for a new field.
        # Poor man's database migrations.
        if "color_class" not in columns:
            conn.execute("ALTER TABLE tasks ADD COLUMN color_class TEXT")

        conn.commit()

        backfill_color_classes()

def add_task(task, scheduled_date=None, color_class="color-1"):
    task_normalized = task.strip().lower()

    conn = get_db()
    cursor = conn.cursor()

    # Check if a task with the same name exists
    cursor.execute("SELECT color_class FROM tasks WHERE LOWER(task) = ?", (task_normalized,))
    existing = cursor.fetchone()

    if existing and existing[0]:
        color_class = existing[0]
    else:
        color_index = hash(task_normalized) % 7 + 1
        color_class = f"color-{color_index}"

    cursor.execute( 
        "INSERT INTO tasks (task, scheduled_date, color_class) VALUES (?, ?, ?)",
        (task, scheduled_date, color_class)
    )
    conn.commit()

def delete_task(task_id):
    conn = get_db()
    conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()

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
    ).fetchall()
    return [Task(*row) for row in rows]

def backfill_color_classes():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, task FROM tasks WHERE color_class IS NULL OR color_class = ''")
    for task_id, task_name in cursor.fetchall():
        color_index = hash(task_name.strip().lower()) % 7 + 1
        color_class = f"color-{color_index}"
        cursor.execute(
            "UPDATE tasks SET color_class = ? WHERE id = ?",
            (color_class, task_id)
        )
    conn.commit()

def get_db():
    if "db" not in g:
        db_file = current_app.config.get("SCHEDULER_DB", "schedule.db")
        g.db = sqlite3.connect(db_file)
    return g.db

def close_db(e=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()