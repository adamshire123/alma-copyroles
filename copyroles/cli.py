import argparse
import os
from sys import exit

import requests
from tabulate import tabulate

from copyroles.alma import AlmaClient

parser = argparse.ArgumentParser()
parser.add_argument("source_user")
parser.add_argument("dest_user")


try:
    apikey = os.environ["ALMA_API_KEY"]
except KeyError:
    exit("MISSING REQUIRED ENVIRONMENT VARIABLE: ALMA_API_KEY")

alma_client = AlmaClient(apikey)


def print_user_roles(roles: list) -> None:
    """Print a nicely formatted table of alma user roles."""
    roles_tab = [
        {
            "status": role["status"]["desc"],
            "role_type": role["role_type"]["desc"],
            "scope": role["scope"].get("desc"),
        }
        for role in roles
    ]
    print(tabulate(roles_tab, headers="keys"))  # noqa: T201


def main() -> None:
    args = parser.parse_args()
    try:
        alma_environment: str = alma_client.get_alma_environment()
    except requests.exceptions.HTTPError as e:
        print("HTTP Error:", e)  # noqa: T201
        exit(1)
    confirm_environment: str = input(
        f"You are working in the \033[1m{alma_environment.upper()}\033[0m environment. "
        "Continue? [y/n]"
    )
    if confirm_environment.lower() == "y":
        source_user: dict = alma_client.get_alma_user(args.source_user)
        dest_user: dict = alma_client.get_alma_user(args.dest_user)
        source_roles: list = source_user["user_role"]
        continue_copy: str = input(
            f"This will copy roles from \033[1m{source_user['primary_id']}\033[0m to "
            f"\033[1m{dest_user['primary_id']}\033[0m. Continue and review roles? [y/n]"
        )
        if continue_copy.lower() == "y":
            review_roles: str = input(
                "would you like to review the roles that will be copied? [y/n]"
            )
            if review_roles.lower() == "y":
                print_user_roles(source_roles)
            while True:
                do_copy: str = input(
                    "Copy these roles? WARNING: This operation cannont be undone. "
                    "[type 'copy-roles' to continue OR 'abort' ] "
                )
                if do_copy.lower() == "copy-roles":
                    alma_client.update_alma_roles(source_roles, dest_user)
                    print("Copy operation initiated.")  # noqa: T201
                    exit()
                if do_copy.lower() == "abort":
                    print("Copy operation cancelled.")  # noqa: T201
                    exit()
