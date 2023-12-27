from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import time
import shutil
import uuid
from cloudwatch_logger import CloudWatchLogger as logger
from aws_secrets import get_secret
from encoding import encode_video_to_base64_response
from base_post_api import make_post_request
from base_get_api import make_get_request
from download_video import download_video
import logging
import warnings
import argparse

parser = argparse.ArgumentParser(description='Run FastAPI server.')
parser.add_argument('--port', type=int, default=3000, help='Port to run the server on')
args = parser.parse_args()

warnings.filterwarnings("ignore")

app = FastAPI()

class TextData(BaseModel):
    text: str
    uid: str

@app.get("/health")
def is_up():
    return {"status": "UP"}

@app.put("/upscale")
def create_video_from_text(data: TextData):
    uid = data.uid
    text = data.text
    try:
        logger.log("Start upscale the video", uid=uid)

        text = data.text
        if not text:
            raise HTTPException(status_code=400, detail="No text provided")

        secret_name = "D-ID"
        secrets = get_secret(secret_name)
        source_url = secrets['freya_source_url']
        authorization = secrets['did_authorization']
        id = make_post_request(text, source_url, authorization, uid=uid)

        logger.log(f"ID after post for the get request is (video_url): {id}", uid=uid)
        logger.log(f"Source URL for the image is: {source_url}", uid=uid)

        max_retries = 100
        retry_interval = 3
        for attempt in range(max_retries):
            logger.log(f"Attempt {attempt + 1}: Trying to get video URL...", uid=uid)
            get_url = f"https://api.d-id.com/talks/{id}"
            video_url = make_get_request(get_url, authorization, uid=uid)

            if video_url:
                logger.log("Video URL retrieved successfully.", uid=uid)
                break
            else:
                logger.log("Video URL not available yet, retrying after 3 seconds...", uid=uid)
                time.sleep(retry_interval)
        else:
            raise HTTPException(status_code=500, detail="Failed to retrieve video URL")

        video_file_name = f'{uid}/video.mp4'
        download_video(video_url, file_name=video_file_name, uid=uid)

        # Encoding video to base64
        response = encode_video_to_base64_response(video_file_name, uid=uid)

        # Clean up: remove the downloaded video file and other temporary files
        logger.log("Start removing UUID dirs", uid=uid)
        os.remove(video_file_name)
        shutil.rmtree(uid)
        logger.log("Finish removing UUID dirs", uid=uid)
        logger.log("Finish upscale the video", uid=uid)
        return response

    except Exception as e:
        logger.log(f"An exception occurred: {e}", level=logging.ERROR, uid=uid)
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=args.port)
