import logging
import os
from threading import Lock

from src.account import Account
from src.notification import Notification


class Notification_Handler:
    _lock = Lock()

    @staticmethod
    def handle_notifications(account: Account, unread_emails: list, preferences: dict):

        with Notification_Handler._lock:

            sound_path = preferences.get("sound")
            os.system(f'paplay "{sound_path}"')

            for mail in unread_emails:
                args = {
                    "title": f"You've got an Email from {mail['from']}",
                    "message": mail["subject"],
                    "application_name": account.email,
                    "urgency": "normal",
                    "path_to_icon": preferences.get("icon"),
                    "path_to_audio": None,
                    "enable_logging": False,
                }

                logging.info(f"Sending notification for {account.email} ...")
                logging.info(f"Mail: {mail}")

                notification = Notification(**args)
                notification.notify()
