"""By Aarish Kodnaney"""

import json
from api_client import APIClient
from stats import StatisticsCalculator

url: str = "https://recruitment.sandboxnu.com/api/eyJkYXRhIjp7ImNoYWxsZW5nZSI6IkZsb3ciLCJlbWFpbCI6ImtvZG5hbmV5LmFAbm9ydGhlYXN0ZXJuLmVkdSIsImR1ZURhdGUiOiIyMDI1LTEyLTE5VDA1OjAwOjAwLjAwMFoifSwiaGFzaCI6Imw3dFpZMVBYUFhkOEZPTVgzNTgifQ"

def main() -> None:
    """
    main function
    """
    # getting data from api
    cl = APIClient(url)
    data = cl.get_data()

    # creating list of participant objects containing relevant info
    list_of_participant_objects = StatisticsCalculator.build_participant_info_list(data)

    # appending json version of those objects to list final_response
    final_response = []
    for participant_object in list_of_participant_objects:
        final_response.append(participant_object.__json__())

    # sorting final response alphabetically by name
    sorted_alphabetically_final_response = sorted(final_response, key=lambda x: x["name"])

    # writing data to output.json
    with open('output.json', 'w') as f:
        json.dump(sorted_alphabetically_final_response, f, indent=2)

    # posting data to api endpoint (this is posting sorted list sorted_alphabetically_final_response, not output.json)
    # output.json is simply for your (the reviewer's) refrence and for me to see my code output
    cl.send_data(url, sorted_alphabetically_final_response)


if __name__ == "__main__":
    main()
