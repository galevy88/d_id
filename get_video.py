import time
from cloudwatch_logger import CloudWatchLogger as logger
from aws_secrets import get_secret
from base_post_api import make_post_request
from base_get_api import make_get_request
from download_video import download_video



def create_video_from_text(text):

    secret_name = "D-ID"
    secrets = get_secret(secret_name)
    source_url = "https://public-global-free-truth-assets.s3.us-east-1.amazonaws.com/High-Res-New-Freya.jpg?response-content-disposition=inline&X-Amz-Security-Token=IQoJb3JpZ2luX2VjELL%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaDGV1LWNlbnRyYWwtMSJGMEQCIEC6%2B0SYZICj9TQoinL0Dh0xKRxR858YtUNStpTAKXkuAiALC4n4fegqrBx51Z5O9Z98hnH%2BJwfsq4%2BVKJp8nCihairoAghbEAAaDDUwMTI0NzgxMDg5MyIMRzY%2F8ZCR%2BVm%2FfJyDKsUCJBeYuGVnL8%2B9cNwBg7JzcwINxgAF9Xl7XOXuOWcfseZS0IkEvSN75L5ZMSxREHEiMx%2FjhoMiCiER0%2B90vcuDsHkwHlt3BtWU7SPBveMotf35jpVHxoiEwYZ1C58aPrEP4xspo2Wi2x%2FKtchtl%2BY6vnm5HtHtbhbHo3XP1OLKtl9%2FvZuR%2BlTBCnN37Ws9kQRx6PSMEhYc0beNK5D9KejA8NhtSzkxYhdcTUOk%2F0L2xnCnT4B5au9otw3GtB3C1oHtbH3C%2Bo5V%2Fq95lzSslek1l%2F%2BcchoV7ha1B1v6zZb6nHeVbmUb49AlgREDs3Rz2DMsUZoT%2B%2FtgmnIc%2BDuqd%2FDtUK9ezNq9aPCc6%2F8QElnvZNY3AhFkT6K4VASxIL0EuTcj4%2F5KsMlbbQNT83xu4McKGcG36HTiTnB6x%2Fz3NDa6LCqB9yl42zDmromtBjq0Ag6VoVWn9yIzktoosezQtDFONQ2lBF%2BZK%2Fdms%2B60iFnoX74jyWYkJpNSX6AzqEszD%2BpviAETh84HGimD1eufA6gf4hmUoLcNdumUM9Uh2%2FkGGbpbzYQg%2FZet3V5v5ENeNiY6uK1Ur3A%2BmUjnsSF486OWq85HR5kFFfQp%2FiQHT39JY%2FeLmiEhVrPNjQCxiVif9IPm7VoJpXaVbNUGES%2Ft1AvQzgazAO0rbNDXl14yDFvnfsU%2BR03VZkrcG4uydMyyu%2BrYTFoMXC910u5SXzgMWwpgn4rVI9iCGJUyvBxX9ecyVbN%2BkUeWz2ur3%2BofHlaihodzWnMoffnuU4thQ8U%2Fpw8GlwPu2sgOLGClEbat%2BrdsH%2B5AHTU8EqyBxZhLbG7U5g6i8CFamxh6c%2F9%2Fi4RK3vhzlcyr&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20240113T102848Z&X-Amz-SignedHeaders=host&X-Amz-Expires=300&X-Amz-Credential=ASIAXJNFSTVG3MQP4XFF%2F20240113%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Signature=aee89b08538106e0327389584c5526f9c1b1d9521193aa4e8b2377bd499b572b"
    authorization = secrets['did_authorization']
    id = make_post_request(text, source_url, authorization, uid="uid")


    max_retries = 100
    retry_interval = 3
    for attempt in range(max_retries):
        logger.log(f"Attempt {attempt + 1}: Trying to get video URL...", uid="uid")
        get_url = f"https://api.d-id.com/talks/{id}"
        video_url = make_get_request(get_url, authorization, uid="uid")

        if video_url:
            logger.log("Video URL retrieved successfully.", uid="uid")
            break
        else:
            logger.log("Video URL not available yet, retrying after 3 seconds...", uid="uid")
            time.sleep(retry_interval)

    video_file_name = f'{"uid"}/video.mp4'
    download_video(video_url, file_name=video_file_name, uid="uid")


if __name__ == "__main__":
    text="Asawi Fredge, Arab ex-minister in the Israeli parliament. Israel has many problems, but it is not an apartheid state.Israel did not expel the Palestinians. Many of them left the combat areas, believing they would return after the war. Those Arabs who stayed were granted full citizenship in Israel with equal rights to Jews."
    create_video_from_text(text)
