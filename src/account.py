import hashlib
import json


class Account:
    def __init__(self, name: str, email: str, sleep: int, pickle: str = None):
        self.name = name
        self.email = email
        self.sleep = sleep
        if not pickle:
            pickle = self.__gethash() + ".pickle"
        self.pickle = pickle

    def __gethash(self):
        """
        Returns a hash of the account's email address.

        This function takes the email address of the account and converts it
        to a hash using the SHA256 algorithm. The hash is then returned.

        Args:
            None

        Returns:
            str: The SHA256 hash of the account's email address.
        """
        unique = self.email
        unique_bytes = unique.encode("utf-8")

        hash_object = hashlib.sha256()
        hash_object.update(unique_bytes)

        hash_bytes = hash_object.digest()
        hash_string = hash_bytes.hex()

        return hash_string

    def to_dict(self):
        """
        Returns a dictionary representation of the object.

        :return: A dictionary containing the name, email and a hash of the credentials.
        :rtype: dict
        """
        return {
            "name": self.name,
            "email": self.email,
            "sleep": self.sleep,
            "pickle": self.pickle,
        }

    def __str__(self):
        """
        Returns a string representation of this object in JSON format.

        :return: A string representation of this object in JSON format.
        :rtype: str
        """
        return json.dumps(self.to_dict(), indent=4)
