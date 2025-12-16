import requests
from participant import Participant, ParticipantStats

# url requests are being made from
url: str = "https://recruitment.sandboxnu.com/api/eyJkYXRhIjp7ImNoYWxsZW5nZSI6IkZsb3ciLCJlbWFpbCI6ImtvZG5hbmV5LmFAbm9ydGhlYXN0ZXJuLmVkdSIsImR1ZURhdGUiOiIyMDI1LTEyLTE5VDA1OjAwOjAwLjAwMFoifSwiaGFzaCI6Imw3dFpZMVBYUFhkOEZPTVgzNTgifQ"

# get request to url and then storing of object in variable response
response = requests.get(url, timeout=20)

# creating json if possible
if response.status_code == 200:
    data = response.json()
else:
    print(f"Error code: {response.status_code}")

def undef() -> list[Participant]:
    to_return: list[Participant] = []
    for participant in data["participantInfo"]:
        to_return.append(Participant(participant["participantId"], participant["name"], [ParticipantStats()], 0, 0))
    return to_return

for participant in undef():
    print(participant)