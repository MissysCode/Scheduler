import sqlite3

DB_NAME = "schedule.db"

def init_db():
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
        if "color_class" not in columns:
            cursor.execute("ALTER TABLE tasks ADD COLUMN color_class TEXT")

        conn.commit()
    backfill_color_classes()

def add_task(task, scheduled_date=None, color_class="color-1"):
    color_index = hash(task.strip().lower()) % 7 + 1
    color_class = f"color-{color_index}"

    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tasks (task, scheduled_date, color_class) VALUES (?, ?, ?)", (task, scheduled_date, color_class))
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
        return cursor.fetchall()
    
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