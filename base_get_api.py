import requests

def make_get_request(url, authorization):
    headers = {
        'Content-Type': 'text/plain',
        'Authorization': authorization
    }

    response = requests.get(url, headers=headers)
    response_json = response.json()
    video_url = response_json["result_url"]
    return video_url
