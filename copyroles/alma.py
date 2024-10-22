import requests
from urllib.parse import urljoin

class AlmaClient():
    def __init__(self, api_key, base_url="https://api-na.hosted.exlibrisgroup.com/almaws/v1/"):
        self.base_url = base_url
        self.headers = {
            "Authorization": f"apikey {api_key}",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }


    def get_alma_user(self, primary_id) -> dict:
        """Get a user record

        args:
            primary_id: The primary ID of a user in Alma (e.g. kerb@mit.edu)
        
        """
        endpoint = "users/" + requests.utils.quote(primary_id)
        response = requests.get(
            urljoin(self.base_url, endpoint),
            headers=self.headers
            )
        response.raise_for_status()
        return response.json()


    def get_alma_environment(self) -> str:
        """Get the alma environment 

        Returns which environment (production or sandbox) the API key is for.
        
        """
        endpoint = "conf/general"
        response = requests.get(
            urljoin(self.base_url, endpoint), 
            headers=self.headers
            )
        response.raise_for_status()
        return response.json()['environment_type']
    

    def update_alma_roles(self, roles, user):
        """Updates the given user object in Alma with the supplied roles"""
        user['user_role'] = roles # the list of roles in the user object is called 'user_role' (yes, singular)
        endpoint = "users/" + requests.utils.quote(user['primary_id'])
        response = requests.put(
            urljoin(self.base_url,endpoint),
            headers=self.headers, json=user
            )
        response.raise_for_status()    
