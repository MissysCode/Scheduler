import sqlite3
from dataclasses import dataclass

DB_NAME = "schedule.db"

@dataclass
class Task:
    task_id: int
    task_name: str
    scheduled_date: str
    color_class: str

def init_db(app):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task TEXT NOT NULL,
                scheduled_date TEXT
            )
        """)
        # Check if 'color_class' column exists
        cursor.execute("PRAGMA table_info(tasks)")
        columns = [col[1] for col in cursor.fetchall()]

        # If you add new fields, you can copy the following code for a new field.
        # Poor man's database migrations.
        if "color_class" not in columns:
            cursor.execute("ALTER TABLE tasks ADD COLUMN color_class TEXT")
        # E.g.
        # if "my_new_field" not in columns:
        #     cursor.execute(...)
        #
        # Also, write a new backfill() function, if approopriate below.
        # Example: backfill_color_classes()
        #
        # If there ever needs to be a type of migration that cannot be done simply
        # by adding a column, then something more sophisticated has to be done here.
        #

        conn.commit()

    backfill_color_classes()

def add_task(task, scheduled_date=None, color_class="color-1"):
    task_normalized = task.strip().lower()

    with sqlite3.connect(DB_NAME) as conn:
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
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()

def assign_task_to_day(task_id, scheduled_date):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE tasks SET scheduled_date = ? WHERE id = ?", (scheduled_date, task_id))
        conn.commit()

def get_all_tasks():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, task, scheduled_date, color_class FROM tasks ORDER BY scheduled_date")
        def to_task(args):
            return Task(*args)
        return map(to_task, cursor.fetchall())

def backfill_color_classes():
    with sqlite3.connect(DB_NAME) as conn:
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