import time
import webbrowser
from threading import Lock

from src.account import Account
from src.notification import Notification


class Notification_Handler:
    _lock = Lock()

    @staticmethod
    def handle_notifications(account: Account, unread_emails: list, preferences: dict):

        with Notification_Handler._lock:

            args = {
                "title": f"{len(unread_emails)} new emails",
                "message": "\n".join([email["subject"] for email in unread_emails[:5]]),
                "application_name": account.email,
                "urgency": "normal",
                "path_to_icon": preferences.get("icon"),
                "path_to_audio": preferences.get("sound"),
                "enable_logging": False,
            }

            notification = Notification(**args)
            notification.notify()

            webbrowser.open(unread_emails[0]["link"])
            time.sleep(5)
