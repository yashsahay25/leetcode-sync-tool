from datetime import datetime

def log(message):
    now = datetime.now().strftime("%H:%M:%S")
    print(f"[{now}] {message}")