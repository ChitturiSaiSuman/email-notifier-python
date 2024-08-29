import atexit
import errno
import logging
import os
import sys

LOCK_FILE = "/tmp/email_notifier_python.lock"


def create_lock_file():
    """
    Creates a lock file containing the current pid, so that only one instance of email_notifier_python can run at a time.
    If a lock file already exists, tries to kill the process with the pid in the file.

    If the process does not exist, removes the stale lock file and tries again.
    If the process exists, prints a message and exits.

    If any other error occurs while trying to create the lock file, raises the exception.
    This function is registered with atexit to remove the lock file when the program exits.
    """
    try:
        file_handle = os.open(LOCK_FILE, os.O_CREAT | os.O_EXCL | os.O_RDWR)
        os.write(file_handle, str(os.getpid()).encode("utf-8"))
        os.close(file_handle)
        atexit.register(remove_lock_file)

    except OSError as e:
        if e.errno == errno.EEXIST:
            with open(LOCK_FILE, "r") as f:
                pid = int(f.read())
            try:
                os.kill(pid, 0)
            except OSError:
                logging.warning(
                    "Stale lock file found. Removing it and trying again ..."
                )
                os.remove(LOCK_FILE)
                create_lock_file()
            else:
                logging.error(
                    "Another instance of email_notifier_python is already running. Exiting ..."
                )
                sys.exit(0)
        else:
            raise


def remove_lock_file():
    try:
        os.remove(LOCK_FILE)
    except OSError:
        pass
