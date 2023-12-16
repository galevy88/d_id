
import base64
from flask import jsonify

import warnings
warnings.filterwarnings("ignore")



def encode_video_to_base64_response(video_path):
    with open(video_path, "rb") as video_file:
        encoded_string = base64.b64encode(video_file.read()).decode()
    return jsonify({"base64_video": encoded_string})


def save_base64_audio(base64_data, file_path):
    # Decode base64 data and write to file
    with open(file_path, "wb") as file:
        file.write(base64.b64decode(base64_data))

