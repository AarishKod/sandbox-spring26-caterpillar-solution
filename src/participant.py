"""By Aarish Kodnaney"""

from typing import List, Any, Dict

class ParticipantStats:
    """
    Represents the stats of a participant

    3 attributes:
        language:
            type: str
            the name of the language

        averageScore:
            type: float
            the average round score the participant had

        averageRoundDuration:
            type: float
            the average round duration the participant had

    1 method:
        return_list:
            returns a list of length 3 with types [str, float, float]
            this list contains a participant's stats for a specific language. The two stats are average
            score and average round duration
    """
    def __init__(self, language: str="", average_score: float=0, average_round_duration: float=0) -> None:
        self.language = language
        self.average_score = average_score
        self.average_round_duration = average_round_duration

    @property
    def as_dict(self) -> Dict[str, Any]:
        """
        returns a list containing the 3 attributes of the object ParticipantStats
        [language, average_score, average_round_duration]
        """
        return {
            "language": self.language,
            "averageScore": self.average_score,
            "averageRoundDuration": self.average_round_duration
        }


class Participant:
    """
    Represents a participant. Has several attributes:

        id: 
            participant's id
            type: int

        name:
            participant's name
            type: str

        languages: 
            list of participant's stats by language
            type: List[ParticipantStats]

            refer to class ParticipantStats for more info

        averageRoundScore:
            average round score across all rounds
            type: float

        averageSessionDuration:
            average session duration across all sessions
            type: float
    """
    def __init__(self, identification: int, name: str, languages: List[ParticipantStats], average_round_score: float, average_session_duration: float) -> None:
        self.id = identification
        self.name = name
        self.languages = languages
        self.average_round_score = average_round_score
        self.average_session_duration = average_session_duration

    def _generate_languages_list(self) -> List[Dict[str, Any]]:
        """
        Generates a list of dicts containing language session info
        """
        list_to_return: List[Dict[str, Any]] = []
        for stat in self.languages:
            list_to_return.append(stat.as_dict)

        return list_to_return


    def __json__(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "languages": self._generate_languages_list(),
            "averageRoundScore": self.average_round_score,
            "averageSessionDuration": self.average_session_duration
        }