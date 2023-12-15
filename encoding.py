
import base64
from flask import jsonify

import warnings
warnings.filterwarnings("ignore")



def encode_video_to_base64_response(video_path):
    with open(video_path, "rb") as video_file:
        encoded_string = base64.b64encode(video_file.read()).decode()
    return jsonify({"base64_video": encoded_string})

