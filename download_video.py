import os
import requests
from cloudwatch_logger import CloudWatchLogger as logger

def download_video(url, file_name):
    logger.log(f"Start download upscaled video from: {url}")
    os.makedirs(os.path.dirname(file_name), exist_ok=True)

    response = requests.get(url)

    if response.status_code == 200:
        with open(file_name, 'wb') as file:
            file.write(response.content)
        return f"Video downloaded as {file_name}"
    else:
        return "Failed to download the video"
