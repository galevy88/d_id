from flask import Flask, request, jsonify
import os
import time
import shutil
from encoding import encode_video_to_base64_response
from base_post_api import make_post_request
from base_get_api import make_get_request
from download_video import download_video
import datetime
import warnings

warnings.filterwarnings("ignore")

app = Flask(__name__)

@app.route('/upscale', methods=['PUT'])
def create_video_from_text():
    current_time = datetime.datetime.now()
    iat = str(int(current_time.timestamp()))
    print(f"IAT {iat}")

    data = request.json
    script_text = data.get("text")
    if not script_text:
        return jsonify({"error": "No text provided"}), 400

    # Your existing code to create and download the video
    source_url = "https://create-images-results.d-id.com/google-oauth2%7C111069582955618623865/upl_Lkv76YmBADLqUYVEr0hgO/image.jpeg"
    authorization = "Basic bmltcm9kLnNhaGFyb2ZAZ21haWwuY29t:sFnfrdwPVo8YQmv0R5hNw"
    id = make_post_request(script_text, source_url, authorization)

    max_retries = 20
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
        return jsonify({"error": "Failed to retrieve video URL"}), 500

    video_file_name = f'{iat}/video.mp4'
    download_video(video_url, file_name=video_file_name)

    # Encoding video to base64
    response = encode_video_to_base64_response(video_file_name)
    print(response)

    # Clean up: remove the downloaded video file and other temporary files
    os.remove(video_file_name)
    shutil.rmtree(iat)

    return response

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3006, debug=True)
