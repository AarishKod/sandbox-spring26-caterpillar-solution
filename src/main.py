"""By Aarish Kodnaney"""

import requests
import json
from typing import Any, List, Dict
from participant import Participant, ParticipantStats

url: str = "https://recruitment.sandboxnu.com/api/eyJkYXRhIjp7ImNoYWxsZW5nZSI6IkZsb3ciLCJlbWFpbCI6ImtvZG5hbmV5LmFAbm9ydGhlYXN0ZXJuLmVkdSIsImR1ZURhdGUiOiIyMDI1LTEyLTE5VDA1OjAwOjAwLjAwMFoifSwiaGFzaCI6Imw3dFpZMVBYUFhkOEZPTVgzNTgifQ"

# get request to url and then storing of object in variable response
response = requests.get(url, timeout=20)

# creating json if possible
if response.status_code == 200:
    data = response.json()
else:
    print(f"Error code: {response.status_code}")


def construct_participant_stats(json_data: Any) -> List[Dict[str, Any]]:
    """"""
    for data_fragment in json_data["sessions"]:

    

def construct_list_of_participants_with_id_name(json_data: Any) -> list[Participant]:
    """
    constructs an incomplete list of participants. All participants will be present, but the dataset
    only contains the correct id and name

    constructors:
        json_data:
            data in json format
            type: Any
    """
    to_return: list[Participant] = []
    for participant in json_data["participantInfo"]:
        to_return.append(Participant(participant["participantId"], participant["name"], [], 0, 0))

    return to_return

incomplete_list = construct_list_of_participants_with_id_name(data)



for participant in incomplete_list:
    print(participant.__json__())