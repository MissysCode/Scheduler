from datetime import datetime

tasks = []

def get_today_schedule():
    today = datetime.now().strftime("%A, %B, %d, %Y")
    print(f"Today's schedule for {today} :\n")
    for task in tasks:
        print(task)

if __name__ == "__main__":
    get_today_schedule()