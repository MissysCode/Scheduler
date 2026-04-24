import os

class Config:
    DATABASE = "schedule.db"
    URL_PREFIX = os.environ.get("SCHEDULER_URL_PREFIX", "")