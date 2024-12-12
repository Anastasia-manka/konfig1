import json
import datetime

class Logger:
    def __init__(self, log_path):
        self.log_path = log_path
        self.logs = []

    def log(self, user, command):
        entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "user": user,
            "command": command
        }
        self.logs.append(entry)
        print(f"Logged command: {command}")  # Отладочное сообщение

    def save(self):
        with open(self.log_path, 'w') as f:
            json.dump(self.logs, f, indent=4)
        print(f"Logs saved to {self.log_path}")  # Отладочное сообщение