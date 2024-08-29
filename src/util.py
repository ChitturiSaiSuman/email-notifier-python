import argparse
import sys


def parse_arguments():
    """
    Parse command line arguments and return them as an argparse.Namespace object.
    The script supports three modes: 'add', 'remove', and 'run'. The 'add' mode is used to add an account, the 'remove' mode is used to remove an account, and the 'run' mode is used to run the script.
    The required arguments for the 'add' mode are '--name' and '--email', which are the name and email address of the user to add.
    The required argument for the 'remove' mode is '--email', which is the email address of the user to remove.
    The optional argument '--sleep' is used to specify the sleep time in seconds. The default value is 60 seconds.
    If any required arguments are missing or if too many arguments are provided, the script exits with a status code of 1.
    Returns:
        argparse.Namespace: An object containing the parsed command line arguments.
    """

    parser = argparse.ArgumentParser(
        description="Script to enable email notifications for Gmail"
    )
    parser.add_argument(
        "mode",
        choices=["add", "remove", "run"],
        help="Mode to run the script in. 'add' to add an account, 'remove' to remove an account, 'run' to run the script.",
    )

    parser.add_argument(
        "--name", type=str, help="Name of the user (required in setup mode)."
    )
    parser.add_argument(
        "--email", type=str, help="Email address of the user (required in setup mode)."
    )
    parser.add_argument(
        "--sleep", type=int, default=60, help="Sleep time in seconds (default: 60)."
    )

    args = parser.parse_args()

    if args.mode == "add":
        if not args.name or not args.email:
            if not args.name:
                sys.stderr.write("Error: Required argument --name is missing\n")
            if not args.email:
                sys.stderr.write("Error: Required argument --email is missing\n")
            sys.exit(1)

    elif args.mode == "remove":
        if not args.email:
            sys.stderr.write("Error: Required argument --email is missing\n")
            sys.exit(1)

    elif args.mode == "run":
        if len(sys.argv) > 2:
            sys.stderr.write("Error: Too many arguments provided\n")
            sys.exit(1)

    return args
