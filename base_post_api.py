import requests
from cloudwatch_logger import CloudWatchLogger as logger

def make_post_request(script_text, source_url, authorization, uid):
    url = "https://api.d-id.com/talks"
    logger.log(f"script_text for the POST request is: {url}", uid=uid)
    payload = {
        "source_url": source_url,
        "driver_url": "bank://subtle/driver-03",
         "script": {
            "type": "text",
            "input": script_text,
            "subtitles": True,
            "provider": {
                "type": "elevenlabs",
                "voice_id": "21m00Tcm4TlvDq8ikWAM"
            },
            "ssml": "false"
        },
        "config": {
            "fluent": "true",
            "pad_audio": 1,
            "stitch": True
        }
    }

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": authorization
    }
    logger.log(f"Sending POST request to: {url}", uid=uid)
    response = requests.post(url, json=payload, headers=headers, verify=False)
    response_json = response.json()
    logger.log(f"Got response from POST request: {response_json}", uid=uid)
    id = response_json["id"]
    return id


