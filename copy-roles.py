import requests
import argparse
import os
from tabulate import tabulate
from sys import exit

parser = argparse.ArgumentParser()
parser.add_argument('source_user')
parser.add_argument('dest_user')
args = parser.parse_args()
base_url = "https://api-na.hosted.exlibrisgroup.com/almaws/v1/"
users_endpoint = 'users/'
config_endpoint = 'conf/'

try:
    apikey = os.getenv('ALMA_API_KEY')
except:
    exit('MISSING REQUIRED ENVIRONMENT VARIABLE: ALMA_API_KEY')
headers = {
    "Authorization": f"apikey {apikey}",
    "Accept": "application/json",
    "Content-Type": "application/json"
}
def get_alma_configuration() -> dict:
    """Retrieve general configuration details. 
    
    Includes an indication of which environment (production or sandbox) the API key is for."""
    url = base_url + config_endpoint + "general"
    response = requests.get(url=url, headers=headers)
    response.raise_for_status
    return response.json()

def get_alma_user(user) -> dict:
    """get an alma user object"""
    url = base_url + users_endpoint + requests.utils.quote(user)
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def get_user_roles(user) -> list:
    """"return a list of roles of an alma user"""
    roles = user.get('user_role')
    return roles

def print_user_roles(roles):
    """Print a nicely formatted table of alma user roles"""
    roles_tab = [{"status": role['status']['desc'], "role_type": role['role_type']['desc'], "scope": role['scope'].get('desc')} for role in roles]
    print(tabulate(roles_tab, headers='keys'))

def update_roles(roles, user):
    """Updates the given user in Alma with the supplied roles"""
    user['user_role'] = roles # the list of roles in the user object is called 'user_role' (yes, singular)
    url = base_url + users_endpoint + requests.utils.quote(user['primary_id'])
    response = requests.put(url, headers=headers, json=user)
    response.raise_for_status()    

alma_configuration = get_alma_configuration()
alma_env_confirm = input(f"You are working in the \033[1m{alma_configuration.get('environment_type').upper()}\033[0m environment. Continue? [y/n]")
if alma_env_confirm.lower() in ["y","yes"]:
    source_user = get_alma_user(args.source_user)
    dest_user = get_alma_user(args.dest_user)
    source_roles = get_user_roles(source_user)
    continue_copy = input(f"This will copy roles from \033[1m{source_user['primary_id']}\033[0m to \033[1m{dest_user['primary_id']}\033[0m. Continue and review roles? [y/n]")
    if continue_copy.lower() in ["y", "yes"]:
        review_roles = input("would you like to review the roles that will be copied? [y/n]")
        if review_roles.lower() in ["y", "yes"]:
            print_user_roles(source_roles)
        do_copy = input("Copy these roles? WARNING: This operation cannont be undone. [copy-roles/n]")
        if do_copy.lower() in ['copy-roles']:
            update_roles(source_roles, dest_user)
                
    



