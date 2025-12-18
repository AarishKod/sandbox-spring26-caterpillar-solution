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



def build_participant_info_list(json_data: Any) -> List[Participant]:
    """
    Builds a list with all info from participant info section of dict
    """
    to_return: List[Participant] = []
    for participant in json_data["participantInfo"]:
        participant_stats = StatisticsCalculator.generate_participant_statistics(json_data, participant["participantId"])
        round_list: List[int] = StatisticsCalculator.get_list_of_rounds(data, participant["participantId"])
        to_return.append(Participant(participant["participantId"], participant["name"], participant_stats, StatisticsCalculator.calculate_average_round_score(data, list_of_rounds=round_list), StatisticsCalculator.calculate_average_session_duration(StatisticsCalculator.generate_list_of_sessions(data, participant["participantId"]))))
    return to_return

if __name__ == "__main__":
    list_of_participant_objects = build_participant_info_list(data)

    final_response = []
    for participant_object in list_of_participant_objects:
        final_response.append(participant_object.__json__())

    sorted_alphabetically_final_response = sorted(final_response, key=lambda x: x["name"])

    with open('output.json', 'w') as f:
        json.dump(sorted_alphabetically_final_response, f, indent=2)

    cl.send_data(url, sorted_alphabetically_final_response)

    

