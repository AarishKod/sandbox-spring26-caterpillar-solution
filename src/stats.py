"""
By Aarish Kodnaney

used for statistical calculation
"""

from typing import List, Dict, Any
from collections import defaultdict
from participant import ParticipantStats, Participant

class StatisticsCalculator():
    """takes care of all stat calculations"""

    @staticmethod
    def calculate_average_round_score(json_data: Any, list_of_rounds: List[int]) -> float | str:
        """
        calculates average round score

        args:
            json_data:
                full data in json format
                type: Any

            list_of_rounds:
                a list of rounds. use StatisticsCalculator.get_list_of_rounds() to generate this
                type: List[int]

        returns:
            average round score if list_of_rounds length != 0. otherwise returns N/A as a string
        """
        sum_of_scores: int = 0
        for round_ in json_data["rounds"]:
            if round_["roundId"] in list_of_rounds:
                sum_of_scores += round_["score"]
        if len(list_of_rounds) != 0:
            return sum_of_scores / len(list_of_rounds)
        return "N/A"

    @staticmethod
    def calculate_average_session_duration(list_of_sessions: List[Dict[str, Any]]) -> float | str:
        """
        calculates average session duration

        args:
            list_of_sessions:
                a list of sessions. use StatisticsCalculator.generate_list_of_sessions() to get this
                type: List[Dict[str, Any]]

        returns:
            average session duration if list_of_sessions length != 0. otherwise returns N/A as a string
        """
        sum_of_durations: float = 0
        for session in list_of_sessions:
            sum_of_durations += session["endTime"] - session["startTime"]
        
        if len(list_of_sessions) != 0:
            return round(sum_of_durations / len(list_of_sessions), 2)
        return "N/A"

    @staticmethod
    def get_list_of_rounds(json_data: Any, participant_id: int) -> List[int]:
        """
        returns a list of ints. each int corresponds to a round

        args:
            json_data:
                full data in json format
                type: Any

            participant_id:
                the id of a participant
                type: int

        returns:
            a list of ints corresponding to rounds in the json for the participant with the given participant id
            type: List[int]
        """
        list_to_return: List[int] = []
        for session in json_data["sessions"]:
            if session["participantId"] == participant_id:
                list_to_return += session["rounds"]

        return list_to_return

    @staticmethod
    def generate_list_of_sessions(json_data: Any, participant_id_number: int) -> List[Dict[Any, Any]]:
        """
        generates a list of all sessions for a given participant id number

        args:
            json_data:
                full data in json format
                type: Any
            
            participant_id_number:
                the id of a participant
                type: int

        returns:
            a list of sessions from the json file. this is a list of dicts
            type: List[Dict[Any, Any]]
        """
        list_of_participant_sessions: List[Dict[Any, Any]] = []
        for session in json_data["sessions"]:
            if session["participantId"] == participant_id_number:
                list_of_participant_sessions.append(session)
        return list_of_participant_sessions

    @staticmethod
    def sort_by_language(sessions: List[Dict[Any, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """
        takes list of sessions for specific participant id number and organizes them by language.

        args:
            sessions:
                a list of sessions from the json file. this is a list of dicts
                type: List[Dict[Any, Any]]

        returns:
            a dict with keys that are languages corresponding to values that are lists of sessions for that respective language
            type: Dict[str, List[Dict[str, Any]]]
        """
        language_sessions = defaultdict(list)
        for session in sessions:
            language_sessions[session["language"]].append(session)
        return dict(language_sessions)

    @staticmethod
    def generate_list_of_participant_statistics_objs(sessions_by_language_arg: Dict[str, List[Dict[str, Any]]], json_data: Any) -> List[ParticipantStats]:
        """
        creates a list of participant statistics objects given a list of sessions by language and the original json file

        args:
            sessions_by_language_arg:
                a dict of sessions sorted by language. use StatisticsCalculator.sort_by_language() and StatisticsCalcualtor.generate_list_of_sessions()
                to build this argument

            json_data:
                full data in json format
                type: Any

        returns:
            a list of ParticipantStats objects initialized with language, avg_score, avg_rd_duration, and the sum of scores (sum only used internally)
            type: List[ParticipantStats]
        """
        list_of_participant_stats_objects: List[ParticipantStats] = []

        # looping through list of sessions ordered by language 
        for session_language in sessions_by_language_arg:
            language = session_language
            rounds: List[int] = []
            round_durations: List[int] = []
            scores: List[int] = []

            # looping through each list of languages at given session language
            for session in sessions_by_language_arg[session_language]:
                rounds += session["rounds"]

            # accumulating scores and times
            for data_fragment_round in json_data["rounds"]:
                if data_fragment_round["roundId"] in rounds:
                    round_durations.append(data_fragment_round["endTime"] - data_fragment_round["startTime"])
                    scores.append(data_fragment_round["score"])

            # calculating average score and average round duration
            avg_score: float = round(sum(scores) / len(scores), 2)
            avg_round_dur: float = round(sum(round_durations) / len(round_durations), 2)

            # adding ParticipantStats object to list of said object. Will be used alter
            list_of_participant_stats_objects.append(ParticipantStats(language, avg_score, avg_round_dur, sum(scores)))

        return list_of_participant_stats_objects

    @staticmethod
    def generate_participant_statistics(json_data: Any, participant_id_number: int) -> List[ParticipantStats]:
        """
        generate statistics for a participant across all languages.
        
        args:
            json_data:
                full data in json format
                type: Any

            participant_id:
                the id of a participant
                type: int
            
        returns:
            list of ParticipantStats objects, (one per language)
            type: List[ParticipantStats]
        """

        calc = StatisticsCalculator

        # we now have a dict of language values with values containing lists of dicts with session info
        sessions_by_language: Dict[str, List[Dict[str, Any]]] = calc.sort_by_language(calc.generate_list_of_sessions(json_data, participant_id_number))
        
        list_of_participant_stats_objects = calc.generate_list_of_participant_statistics_objs(sessions_by_language, json_data)

        # sorting list by score in ascending order prior to return
        to_return = sorted(list_of_participant_stats_objects, key=lambda x: x.total_score, reverse=True)

        return to_return

    @staticmethod
    def build_participant_info_list(json_data: Any) -> List[Participant]:
        """
        Builds a list with all info from participant info section of dict

        args:
            json_data:
                full data in json format
                type: Any

        returns:
            list of Participant objects initialized with all values
            type: List[Participant]
        """
        to_return: List[Participant] = []
        for participant in json_data["participantInfo"]:
            participant_stats = StatisticsCalculator.generate_participant_statistics(json_data, participant["participantId"])
            round_list: List[int] = StatisticsCalculator.get_list_of_rounds(json_data, participant["participantId"])
            to_return.append(Participant(participant["participantId"], participant["name"], participant_stats, StatisticsCalculator.calculate_average_round_score(json_data, list_of_rounds=round_list), StatisticsCalculator.calculate_average_session_duration(StatisticsCalculator.generate_list_of_sessions(json_data, participant["participantId"]))))
        return to_return
