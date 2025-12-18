# Data Definition: Participant Statistics
by aarish kodnaney

## **Participant:**
    A participant is an object with this structure

    {
        participantId: int                  (unique identifier for a participant)
        name: str                           (name of participant)
        languages: List[ParticipantStats]   (list of statistics for each language a participant spent time on)
        averageRoundScore: float | str      (overall average round score for all languages. N/A if 0 rounds)
        averageSessionDuration: float | str (overall average session duration. N/A if 0 rounds)
    }

## **ParticipantStat:**
    An object with this structure
    {
        language: str                        (language name)
        averageScore: int                    (average score for this language)
        averageRoundDuration: int             (average round duration for this language)
    }

## **Constraints:**
    - All numeric values must be rounded to two decimal places
    - If languages empty, avgRoundScore and avgSessionDuration must be "N/A"