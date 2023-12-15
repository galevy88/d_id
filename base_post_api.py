import requests

def make_post_request(script_text, source_url, authorization):
    url = "https://api.d-id.com/talks"

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

    response = requests.post(url, json=payload, headers=headers)
    response_json = response.json()
    id = response_json["id"]
    return id



