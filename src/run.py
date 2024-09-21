import logging
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta
from traceback import format_exc

from googleapiclient.discovery import build
from google.auth.exceptions import RefreshError

from src.account import Account
from src.account_manager import Account_Manager
from src.auth import Authenticator
from src.client import Client
from src.constants_manager import Constants
from src.notification_handler import Notification_Handler


class EmailNotifier:
    def __init__(self):
        self.accounts_to_watch = Account_Manager.get_all_accounts()

    def run(self):
        if not self.accounts_to_watch:
            logging.warning("No accounts to watch. Exiting ...")
            return

        with ThreadPoolExecutor(max_workers=len(self.accounts_to_watch)) as executor:
            futures = [
                executor.submit(self.watch, account)
                for account in self.accounts_to_watch
            ]

            for future in futures:
                future.result()

    def watch(self, account: Account):
        creds = Authenticator.verify_creds(account)
        service = build("gmail", "v1", credentials=creds)
        client = Client(service)
        preferences = Constants().get("preferences").get(account.email, {})

        while True:
            try:
                last_checked = Account_Manager.get_last_checked(account)

                unread_emails = client.get_unread_emails(last_checked)
                last_checked = datetime.now() - timedelta(seconds=1)

                unread_emails = self.apply_preferences(unread_emails, preferences)

                if unread_emails:
                    Notification_Handler.handle_notifications(
                        account, unread_emails, preferences
                    )

                Account_Manager.set_last_checked(account, last_checked)

            except RefreshError:
                logging.error(f"Error in account {account.email}: {format_exc()}")
                creds = Authenticator.verify_creds(account)
                service = build("gmail", "v1", credentials=creds)
                client = Client(service)


            except Exception as e:
                logging.error(f"Error in account {account.email}: {format_exc()}")

            time.sleep(account.sleep)

    def apply_preferences(self, unread_emails: list, preferences: dict):
        watch_tags = preferences.get("watch", [])
        ignore_tags = preferences.get("ignore", [])

        unread_emails = filter(
            lambda email: not any(
                tag.lower() in email["subject"].lower()
                or tag.lower() in email["from"].lower()
                for tag in ignore_tags
            ),
            unread_emails,
        )

        if not unread_emails:
            return []

        unread_emails = sorted(
            unread_emails,
            key=lambda email: sum(
                tag.lower() in email["subject"].lower()
                or tag.lower() in email["from"].lower()
                for tag in watch_tags
            ),
            reverse=True,
        )

        return unread_emails


def main():
    notifier = EmailNotifier()
    notifier.run()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
