import logging
import os
from datetime import datetime, timedelta

from src.account import Account
from src.auth import Authenticator
from src.constants_manager import Constants


class Account_Manager:
    @staticmethod
    def add_account(name: str, email: str, sleep: int):
        logging.info(f"Adding account for {email} ...")

        all_accounts = Account_Manager.get_all_accounts()

        for account in all_accounts:
            if account.email == email:
                raise Exception("Account already exists")

        account = Account(name, email, sleep)
        creds = Authenticator.authenticate(account)

        Authenticator.dump_creds(account, creds)

        all_accounts = list(map(lambda account: account.to_dict(), all_accounts))
        all_accounts.append(account.to_dict())

        # Add account to config
        const_instance = Constants()
        const_instance.acquire_lock()
        config = const_instance.get("config")
        config["accounts"] = all_accounts
        const_instance.set("config", config)
        const_instance.release_lock()

        # Set last checked time
        delta_config = config.get("default_time_delta")
        days = delta_config.get("days", 0)
        weeks = delta_config.get("weeks", 0)
        months = delta_config.get("months", 0)
        total_days = days + weeks * 7 + months * 30
        delta = timedelta(days=total_days)
        last_checked_time = datetime.now() - delta

        Account_Manager.set_last_checked(account, last_checked_time)

    @staticmethod
    def remove_account(email: str):
        logging.info(f"Removing account for {email} ...")

        all_accounts = Account_Manager.get_all_accounts()

        for account in all_accounts:
            if account.email == email:
                all_accounts.remove(account)
                break

        all_accounts = list(map(lambda account: account.to_dict(), all_accounts))

        # Remove account from config
        const_instance = Constants()
        const_instance.acquire_lock()
        config = const_instance.get("config")
        config["accounts"] = all_accounts
        const_instance.set("config", config)
        const_instance.release_lock()

        # Delete creds
        Authenticator.delete_creds(account)

        # Remove last checked time
        Account_Manager.remove_last_checked(account)

    @staticmethod
    def get_all_accounts() -> list[Account]:
        const_instance = Constants()
        const_instance.acquire_lock()

        config = const_instance.get("config")
        all_accounts = config.get("accounts", [])

        const_instance.release_lock()

        all_accounts = list(map(lambda account: Account(**account), all_accounts))

        return all_accounts

    @staticmethod
    def get_last_checked(account: Account) -> datetime:
        filename = account.email
        filepath = os.path.join('cache', filename)
        with open(filepath) as f:
            last_checked = f.read()
            return datetime.fromisoformat(last_checked)

    @staticmethod
    def set_last_checked(account: Account, last_checked: datetime):
        filename = account.email
        filepath = os.path.join('cache', filename)
        with open(filepath, "w") as f:
            f.write(last_checked.isoformat())

    @staticmethod
    def remove_last_checked(account: Account):
        filename = account.email
        filepath = os.path.join('cache', filename)
        os.remove(filepath)
