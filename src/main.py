"""By Aarish Kodnaney"""

import requests
import json
from typing import Any, List, Dict
from participant import Participant, ParticipantStats
from collections import defaultdict

url: str = "https://recruitment.sandboxnu.com/api/eyJkYXRhIjp7ImNoYWxsZW5nZSI6IkZsb3ciLCJlbWFpbCI6ImtvZG5hbmV5LmFAbm9ydGhlYXN0ZXJuLmVkdSIsImR1ZURhdGUiOiIyMDI1LTEyLTE5VDA1OjAwOjAwLjAwMFoifSwiaGFzaCI6Imw3dFpZMVBYUFhkOEZPTVgzNTgifQ"

# get request to url and then storing of object in variable response
response = requests.get(url, timeout=20)

# creating json if possible
if response.status_code == 200:
    data = response.json()
else:
    print(f"Error code: {response.status_code}")
    data = None

def generate_participant_statistics(json_data: Any, participant_id_number: int) -> List[ParticipantStats]:
    """
    Given a json file and participantId number, it returns a list of all the ParticipantStats objects constructed
    respective to 
    """

    def generate_list_of_sessions() -> List[Dict[Any, Any]]:
        """
        Generates a list of all sessions for a given participant id number
        """
        list_of_participant_sessions: List[Dict[Any, Any]] = []
        for session in json_data["sessions"]:
            if session["participantId"] == participant_id_number:
                list_of_participant_sessions.append(session)
        return list_of_participant_sessions

    def sort_by_language(sessions: List[Dict[Any, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """
        Takes list of sessions for specific participant id number and organizes them by language. 
        Output format is something like this:
        "French": [
            {
                "participantId": 0,
                "sessionId": 0,
                "language": "French",
                "rounds": [0],
                "startTime": 1650328640,
                "endTime": 1650328740

            },
            {
                "participantId": 0,
                "sessionId": 2,
                "language": "French",
                "rounds": [3],
                "startTime": 1650328640,
                "endTime": 1650328740
            },
        ],
        "German": [
            {
                "participantId": 0,
                "sessionId": 3,
                "language": "German",
                "rounds": [4],
                "startTime": 1650328640,
                "endTime": 1650328740
            },
        ]
        """
        language_sessions = defaultdict(list)
        for session in sessions:
            language_sessions[session["language"]].append(session)
        return dict(language_sessions)

    # we now have a dict of language values with values containing lists of dicts with session info
    sessions_by_language: Dict[str, List[Dict[str, Any]]] = sort_by_language(generate_list_of_sessions())
    list_of_participant_stats_objects: List[ParticipantStats] = []

    for session_language in sessions_by_language:
        language = session_language
        rounds: List[int] = []
        round_durations: List[int] = []
        scores: List[int] = []
        for session in sessions_by_language[session_language]:
            rounds += session["rounds"]

        # accumulating scores and times
        for data_fragment_round in json_data["rounds"]:
            if data_fragment_round["roundId"] in rounds:
                round_durations.append(data_fragment_round["endTime"] - data_fragment_round["startTime"])
                scores.append(data_fragment_round["score"])

        # calculating average score and average round duration
        avg_score: float = round(sum(scores)/len(scores), 2)
        avg_round_dur: float = round(sum(round_durations)/len(round_durations), 2)

        list_of_participant_stats_objects.append(ParticipantStats(language, avg_score, avg_round_dur))


    return list_of_participant_stats_objects
    
def calculate_average_round_score(participant_statistics: List[ParticipantStats]) -> float:
    sum_of_scores: float = 0
    for statistic in participant_statistics:
        sum_of_scores += statistic.average_score
    
    if len(participant_statistics) is not 0:
        return round(sum_of_scores / len(participant_statistics), 2)
    return 0

def calculate_average_session_duration(participant_statistics: List[ParticipantStats]) -> float:
    sum_of_durations: float = 0
    for statistic in participant_statistics:
        sum_of_durations += statistic.average_round_duration
    
    if len(participant_statistics) is not 0:
        return round(sum_of_durations / len(participant_statistics), 2)
    return 0

def build_participant_info_list(json_data: Any) -> List[Participant]:
    """
    Builds a list with all info from participant info section of dict
    """
    to_return: List[Participant] = []
    for participant in json_data["participantInfo"]:
        participant_stats = generate_participant_statistics(json_data, participant["participantId"])
        to_return.append(Participant(participant["participantId"], participant["name"], participant_stats, calculate_average_round_score(participant_stats), calculate_average_session_duration(participant_stats)))
    return to_return

if __name__ == "__main__":
    lt = build_participant_info_list(data)

    final_response = []
    for value in lt:
        final_response.append(value.__json__())

    with open('output.json', 'w') as f:
        json.dump(final_response, f, indent=2)

    

