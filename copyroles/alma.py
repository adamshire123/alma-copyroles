from urllib.parse import quote, urljoin

import requests


class AlmaClient:
    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api-na.hosted.exlibrisgroup.com/almaws/v1/",
    ) -> None:
        self.base_url = base_url
        self.api_key = api_key
        self.headers = {
            "Authorization": f"apikey {self.api_key}",
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

    @property
    def alma_environment(self) -> str:
        """Returns which environment (production or sandbox) the API key is for."""
        endpoint = "conf/general"
        response = requests.get(
            urljoin(self.base_url, endpoint), headers=self.headers, timeout=10
        )
        response.raise_for_status()
        return response.json()["environment_type"]

    def update_alma_roles(self, new_roles: list, target_user: dict) -> None:
        """Updates the given user object in Alma with the supplied roles."""
        target_user["user_role"] = (
            # the list of roles in the user object is called 'user_role' (yes, singular)
            new_roles
        )
        endpoint = "users/" + quote(target_user["primary_id"])
        response = requests.put(
            urljoin(self.base_url, endpoint),
            headers=self.headers,
            json=target_user,
            timeout=10,
        )
        response.raise_for_status()

    def create_alma_user(self, user_record: dict) -> None:
        """Creates an alma user from a user record."""
        endpoint = "users/"
        response = requests.post(
            urljoin(self.base_url, endpoint),
            headers=self.headers,
            json=user_record,
            timeout=10,
        )
        response.raise_for_status()
