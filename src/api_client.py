"""
By Aarish Kodnaney

this is an api client for fetching data from the endpoint
"""

from typing import Any
import requests

class APIClient:
    """API Communication"""

    def __init__(self, base_url: str, timeout: int = 20) -> None:
        self.base_url = base_url
        self.timeout = timeout

    def get_data(self) -> Any:
        """
        Fetches data from the API.

        returns:
            either JSON data as a dict or None if request fails. If request fails,
            will print out error code
        """

        try:
            response = requests.get(self.base_url, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as error:
            print(f"Error: {error}")
            return None

    def send_data(self, api_url: str, payload: Any) -> None:
        """
        Will send data to the endpoint

        args:
            api_url: str -> the actual endpoint
            payload: Any -> what we're posting to the api

        returns:
            nothing
            refer to print statements below for notifiers
        """
        try:
            response = requests.post(api_url, json=payload, timeout=20)

            print(f"Status code: {response.status_code}")
            print(f"Response body (json): {response.json()}")
            print(f"Response body (text): {response.text}")
        except requests.exceptions.RequestException as error:
            print(f"Error: {error}")
