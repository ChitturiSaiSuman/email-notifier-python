import logging

from src.account_manager import Account_Manager
from src.constants_manager import Constants
from src.instance_handler import create_lock_file
from src.run import main
from src.util import parse_arguments

if __name__ == "__main__":

    create_lock_file()

    args = parse_arguments()

    if args.mode == "add" or args.mode == "remove":
        LOG_FILE = Constants().get("config").get("setup.log")
        log_mode = "a"  # append mode
    else:
        LOG_FILE = Constants().get("config").get("run.log")
        log_mode = "w"  # write mode

    logging.basicConfig(
        format="%(asctime)s,%(msecs)03d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s",
        datefmt="%Y-%m-%d:%H:%M:%S",
        level=logging.INFO,
        filename=LOG_FILE,
        filemode=log_mode,
    )

    if args.mode == "add":
        name, email, sleep = args.name, args.email, args.sleep
        Account_Manager.add_account(name, email, sleep)

    elif args.mode == "remove":
        email = args.email
        Account_Manager.remove_account(email)

    elif args.mode == "run":
        logging.info("Running ...")

        main()
