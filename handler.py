import time
from base_post_api import make_post_request
from base_get_api import make_get_request
from download_video import download_video

script_text = "Hi My name is Nimi"
source_url = "https://create-images-results.d-id.com/google-oauth2%7C111069582955618623865/upl_Lkv76YmBADLqUYVEr0hgO/image.jpeg"
authorization = "Basic xxx"

id = make_post_request(script_text, source_url, authorization)

print(f"Sleeping 20 sec")
time.sleep(20)

get_url = f"https://api.d-id.com/talks/{id}"

video_url = make_get_request(get_url, authorization)

download_video(video_url, file_name='video.mp4')


