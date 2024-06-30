from .logger import logger
import json
from datetime import datetime


class MemorySystem:
    def __init__(self, memory_file="conversation_memory.json"):
        self.memory_file = memory_file
        self.current_session = []
        self.load_memory()

    def load_memory(self):
        try:
            with open(self.memory_file, "r") as f:
                self.all_sessions = json.load(f)
        except FileNotFoundError:
            self.all_sessions = {}

    def save_memory(self):
        with open(self.memory_file, "w") as f:
            json.dump(self.all_sessions, f)

    def add_to_current_session(self, entry):
        self.current_session.append(entry)

    def end_current_session(self, user_id):
        if self.current_session:
            timestamp = datetime.now().isoformat()
            if user_id not in self.all_sessions:
                self.all_sessions[user_id] = []
            self.all_sessions[user_id].append(
                {"timestamp": timestamp, "conversation": self.current_session}
            )
            self.save_memory()
            self.current_session = []

    def get_current_session(self):
        return self.current_session

    def get_user_sessions(self, user_id):
        return self.all_sessions.get(user_id, [])

    def get_last_n_sessions(self, user_id, n):
        user_sessions = self.get_user_sessions(user_id)
        return user_sessions[-n:]

    def clear_user_memory(self, user_id):
        if user_id in self.all_sessions:
            del self.all_sessions[user_id]
            self.save_memory()


memory_system = MemorySystem()
