import os
import requests
from typing import Optional

class SuccessVideosApi:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def search_success_videos(self, input_text: str, k: int, industry: Optional[str] = None) -> dict:
        """
        Make a POST request to the specified endpoint with the given parameters.

        Args:
            endpoint (str): The URL of the endpoint to send the POST request to.
            input_text (str): The input text for the request.
            k (int): The number of results to return.
            industry (Optional[str]): The industry to filter by. If None or empty, no filter is applied.

        Returns:
            dict: The JSON response from the API.

        Raises:
            requests.RequestException: If there's an error with the request.
        """
        # Prepare the base request body
        body = {
            "input": input_text,
            "config": {
                "configurable": {
                    "search-parameters": {
                        "k": k
                    }
                }
            }
        }

        # Add the industry filter if provided
        if industry:
            body["config"]["configurable"]["search-parameters"]["filter"] = {
                "must": [
                    {
                        "key": "metadata.industry",
                        "match": {
                            "value": industry
                        }
                    }
                ]
            }
        return self.request("POST", "search_success_videos_chain/invoke", json=body)["output"]
    
    def industries(self) -> dict:
        """
        Make a GET request to the specified endpoint with the given parameters.

        Args:
            endpoint (str): The URL of the endpoint to send the POST request to.

        Returns:
            dict: The JSON response from the API.

        Raises:
            requests.RequestException: If there's an error with the request.
        """
        return self.request("GET", "industries")["industries"]

    def request(self, method: str, endpoint: str, *args, **kwargs) -> dict:
        try:
            url = os.path.join(self.base_url, endpoint)
            req_fn = getattr(requests, method.lower())
            response = req_fn(url, *args, **kwargs)
            response.raise_for_status()  # Raise an exception for bad status codes
            return response.json()
        except requests.RequestException as e:
            # Log the error (you might want to use a proper logging system in a real app)
            print(f"Error making POST request: {e}")
            raise
