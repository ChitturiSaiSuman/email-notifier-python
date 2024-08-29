import json
import logging
import os
import threading


class Constants:
    def __init__(self):
        self.file_paths = {
            "cache": "../cache.json",
            "config": "../config.json",
            "client_secret": "../client_secret.json",
            "preferences": "../preferences.json",
        }
        self._lock = threading.Lock()

    def acquire_lock(self):
        self._lock.acquire()

    def release_lock(self):
        self._lock.release()

    def get(self, key: str):
        if not self.file_paths.get(key):
            logging.error("Invalid constant key: " + key)
            raise Exception("Invalid constant key: " + key)

        relative_path = os.path.join(os.path.dirname(__file__), self.file_paths[key])
        absolute_path = os.path.abspath(relative_path)

        with open(absolute_path, "r") as f:
            return json.load(f)

    def set(self, key: str, value: dict):
        if not self.file_paths.get(key):
            logging.error("Invalid constant key: " + key)
            raise Exception("Invalid constant key: " + key)

        relative_path = os.path.join(os.path.dirname(__file__), self.file_paths[key])
        absolute_path = os.path.abspath(relative_path)

        with open(absolute_path, "w") as f:
            json.dump(value, f, indent=4)
