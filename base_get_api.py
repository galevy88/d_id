import requests

def make_get_request(url, authorization):
    headers = {
        "accept": "application/json",
        "content-type": 'text/plain',
        "authorization": authorization
    }

    response = requests.get(url, headers=headers)
    response_json = response.json()

    # Check if 'result_url' is in the response
    if 'result_url' in response_json:
        video_url = response_json['result_url']
        return video_url
    else:
        # Return None or a custom message if 'result_url' is not present
        return None

