import requests
from cloudwatch_logger import CloudWatchLogger as logger

def make_get_request(url, authorization, uid):
    headers = {
        "accept": "application/json",
        "content-type": 'text/plain',
        "authorization": authorization
    }
    logger.log(f"Sending GET request to: {url}", uid=uid)
    response = requests.get(url, headers=headers, verify=False)
    response_json = response.json()
    logger.log(f"Got response from GET request: {response_json}", uid=uid)
    # Check if 'result_url' is in the response
    if 'result_url' in response_json:
        video_url = response_json['result_url']
        return video_url
    else:
        return None

