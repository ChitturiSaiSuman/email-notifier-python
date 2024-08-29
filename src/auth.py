import logging
import os
import pickle

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

from src.account import Account
from src.constants_manager import Constants


class Authenticator:
    @staticmethod
    def authenticate(account: Account) -> Credentials:

        logging.info(f"Authenticating for {account.email} ...")

        const_instance = Constants()
        client_secret = const_instance.get("client_secret")
        client_config = client_secret.get("client_config")
        SCOPES = client_secret.get("scopes")

        flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
        creds = flow.run_local_server(port=0)

        return creds

    @staticmethod
    def verify_creds(account: Account):
        creds = Authenticator.get_creds(account)
        if not creds.valid and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            Authenticator.dump_creds(account, creds)
        return creds

    @staticmethod
    def get_creds(account: Account) -> Credentials:
        file_name = account.pickle
        file_dir = "../pickles"
        relative_path = os.path.join(os.path.dirname(__file__), file_dir, file_name)
        absolute_path = os.path.abspath(relative_path)

        with open(absolute_path, "rb") as token:
            creds = pickle.load(token)

        return creds

    @staticmethod
    def dump_creds(account: Account, creds: Credentials):
        file_name = account.pickle
        file_dir = "../pickles"
        relative_path = os.path.join(os.path.dirname(__file__), file_dir, file_name)
        absolute_path = os.path.abspath(relative_path)

        with open(absolute_path, "wb") as token:
            pickle.dump(creds, token)

    @staticmethod
    def delete_creds(account: Account):
        file_name = account.pickle
        file_dir = "../pickles"
        relative_path = os.path.join(os.path.dirname(__file__), file_dir, file_name)
        absolute_path = os.path.abspath(relative_path)

        os.remove(absolute_path)
