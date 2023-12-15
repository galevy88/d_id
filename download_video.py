import os
import requests

def download_video(url, file_name):
    # Ensure the directory exists
    os.makedirs(os.path.dirname(file_name), exist_ok=True)

    response = requests.get(url)

    if response.status_code == 200:
        with open(file_name, 'wb') as file:
            file.write(response.content)
        return f"Video downloaded as {file_name}"
    else:
        return "Failed to download the video"
