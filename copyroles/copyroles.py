import requests
import argparse
import os
from tabulate import tabulate
from sys import exit
from copyroles.alma import AlmaClient

parser = argparse.ArgumentParser()
parser.add_argument('source_user')
parser.add_argument('dest_user')



try:
    apikey = os.environ['ALMA_API_KEY']
except:
    exit('MISSING REQUIRED ENVIRONMENT VARIABLE: ALMA_API_KEY')

almaclient = AlmaClient(apikey)

def print_user_roles(roles):
    """Print a nicely formatted table of alma user roles"""
    roles_tab = [{"status": role['status']['desc'], "role_type": role['role_type']['desc'], "scope": role['scope'].get('desc')} for role in roles]
    print(tabulate(roles_tab, headers='keys'))


def main ():
    args = parser.parse_args()
    try: 
        alma_environment = lma.get_alma_environment()
    except requests.exceptions.HTTPError as e:
        exit(e)
    confirm_environment = input(f"You are working in the \033[1m{alma_environment.upper()}\033[0m environment. Continue? [y/n]")
    if confirm_environment.lower() == "y":
        source_user = get_alma_user(args.source_user)
        dest_user = get_alma_user(args.dest_user)
        source_roles = source_user.get('user_role')
        continue_copy = input(f"This will copy roles from \033[1m{source_user['primary_id']}\033[0m to \033[1m{dest_user['primary_id']}\033[0m. Continue and review roles? [y/n]")
        if continue_copy.lower() == "y":
            review_roles = input("would you like to review the roles that will be copied? [y/n]")
            if review_roles.lower() == "y":
                print_user_roles(source_roles)
            do_copy = input("Copy these roles? WARNING: This operation cannont be undone. [copy-roles/n]")
            if do_copy.lower() in ['copy-roles']:
                update_alma_roles(source_roles, dest_user)
                
    
if __name__ == "__main__":
    main()


