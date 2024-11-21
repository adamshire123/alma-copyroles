from urllib.parse import quote, urljoin

import requests


class AlmaClient:
    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api-na.hosted.exlibrisgroup.com/almaws/v1/",
    ) -> None:
        self.base_url = base_url
        self.headers = {
            "Authorization": f"apikey {api_key}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

    def get_alma_user(self, primary_id: str) -> dict:
        """Get a user record.

        Args:
            primary_id: The primary ID of a user in Alma (e.g. kerb@mit.edu)

        """
        endpoint = "users/" + quote(primary_id)
        response = requests.get(
            urljoin(self.base_url, endpoint), headers=self.headers, timeout=10
        )
        response.raise_for_status()
        return response.json()

    def get_alma_environment(self) -> str:
        """Get the alma environment.

        Returns which environment (production or sandbox) the API key is for.

        """
        endpoint = "conf/general"
        response = requests.get(
            urljoin(self.base_url, endpoint), headers=self.headers, timeout=10
        )
        response.raise_for_status()
        return response.json()["environment_type"]

    def update_alma_roles(self, new_roles: list, user_to_update: dict) -> None:
        """Updates the given user object in Alma with the supplied roles."""
        user_to_update["user_role"] = (
            # the list of roles in the user object is called 'user_role' (yes, singular)
            new_roles
        )
        endpoint = "users/" + quote(user_to_update["primary_id"])
        response = requests.put(
            urljoin(self.base_url, endpoint),
            headers=self.headers,
            json=user_to_update,
            timeout=10,
        )
        response.raise_for_status()
