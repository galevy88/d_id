from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import time
import shutil
from aws_secrets import get_secret
from encoding import encode_video_to_base64_response
from base_post_api import make_post_request
from base_get_api import make_get_request
from download_video import download_video
import warnings
import uuid


warnings.filterwarnings("ignore")

app = FastAPI()

class TextData(BaseModel):
    text: str

@app.get("/health")
def is_up():
    return {"status": "UP"}

@app.put("/upscale")
def create_video_from_text(data: TextData):
    
    iat = str(uuid.uuid4())
    print(f"IAT {iat}")

    text = data.text
    if not text:
        raise HTTPException(status_code=400, detail="No text provided")

    secret_name = "D-ID"
    secrets = get_secret(secret_name)
    source_url = secrets['freya_source_url']
    authorization = secrets['did_authorization']
    id = make_post_request(text, source_url, authorization)

    print(f"ID {id}")
    print(f"source_url {source_url}")

    max_retries = 100
    retry_interval = 3
    for attempt in range(max_retries):
        print(f"Attempt {attempt + 1}: Trying to get video URL...")
        get_url = f"https://api.d-id.com/talks/{id}"
        video_url = make_get_request(get_url, authorization)

        if video_url:
            print("Video URL retrieved successfully.")
            break
        else:
            print("Video URL not available yet, retrying after 3 seconds...")
            time.sleep(retry_interval)
    else:
        raise HTTPException(status_code=500, detail="Failed to retrieve video URL")

    video_file_name = f'{iat}/video.mp4'
    download_video(video_url, file_name=video_file_name)

    # Encoding video to base64
    response = encode_video_to_base64_response(video_file_name)

    # Clean up: remove the downloaded video file and other temporary files
    os.remove(video_file_name)
    shutil.rmtree(iat)

    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3000)
