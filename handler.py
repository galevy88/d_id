import time
from aws_secrets import get_secret
from base_post_api import make_post_request
from base_get_api import make_get_request
from download_video import download_video

### Secrets ###
secret_name = "D-ID-D2efUj"
secrets = get_secret(secret_name)

source_url = secrets['freya_source_url']
authorization = secrets['did_authorization']

script_text = "Hi My name is Nimi and Im in love with Galchuk"

id = make_post_request(script_text, source_url, authorization)

print(f"Sleeping 20 sec")
time.sleep(20)

get_url = f"https://api.d-id.com/talks/{id}"

video_url = make_get_request(get_url, authorization)

download_video(video_url, file_name='video.mp4')


