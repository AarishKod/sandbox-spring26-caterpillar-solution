"""By Aarish Kodnaney"""

import json
from typing import Any, List, Dict
from collections import defaultdict
import requests
from participant import Participant, ParticipantStats
from api_client import APIClient
from stats import StatisticsCalculator

url: str = "https://recruitment.sandboxnu.com/api/eyJkYXRhIjp7ImNoYWxsZW5nZSI6IkZsb3ciLCJlbWFpbCI6ImtvZG5hbmV5LmFAbm9ydGhlYXN0ZXJuLmVkdSIsImR1ZURhdGUiOiIyMDI1LTEyLTE5VDA1OjAwOjAwLjAwMFoifSwiaGFzaCI6Imw3dFpZMVBYUFhkOEZPTVgzNTgifQ"

# getting data from api
cl = APIClient(url)
data = cl.get_data()

def main() -> None:
    """
    main function
    """
    list_of_participant_objects = StatisticsCalculator.build_participant_info_list(data)
    final_response = []
    for participant_object in list_of_participant_objects:
        final_response.append(participant_object.__json__())

    sorted_alphabetically_final_response = sorted(final_response, key=lambda x: x["name"])
    with open('output.json', 'w') as f:
        json.dump(sorted_alphabetically_final_response, f, indent=2)

    cl.send_data(url, sorted_alphabetically_final_response)

if __name__ == "__main__":
    main()

    

