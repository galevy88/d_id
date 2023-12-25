
import base64
from cloudwatch_logger import CloudWatchLogger as logger

import warnings
warnings.filterwarnings("ignore")



def encode_video_to_base64_response(video_path):
    logger.log(f"Start encoding video to base64")
    with open(video_path, "rb") as video_file:
        encoded_string = base64.b64encode(video_file.read()).decode()
    logger.log(f"Finished encode video")
    logger.log(f"Saving encoded video to: {video_path}")
    return {"base64_video": encoded_string}


def save_base64_audio(base64_data, file_path):
    logger.log(f"Start saving video from base64")
    with open(file_path, "wb") as file:
        file.write(base64.b64decode(base64_data))
    logger.log(f"Saving base64 to a video to path: {file_path}")

