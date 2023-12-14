import requests

def make_post_request(script_text, source_url, authorization):
    url = "https://api.d-id.com/talks"

    payload = {
        "source_url": source_url,
        "script": {
            "type": "text",
            "input": script_text
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

