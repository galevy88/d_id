import requests
import base64
msg = {
    "text": "This Is message the called from the api bot - via visual studio code"
}
def call_api_and_save_video():
    url = "http://3.89.90.148:3006/upscale"
    headers = {"Content-Type": "application/json"}
    data = msg

    # Sending PUT request to the API
    response = requests.put(url, json=data, headers=headers)

    if response.status_code == 200:
        # Extracting base64 encoded video data from response
        video_data_base64 = response.json().get("base64_video")
        if video_data_base64:
            # Decoding base64 to binary data
            video_binary_data = base64.b64decode(video_data_base64)

            # Writing binary data to MP4 file
            with open("video_final.mp4", "wb") as video_file:
                video_file.write(video_binary_data)
            print("Video saved as video_final.mp4")
        else:
            print("No video data found in response")
    else:
        print(f"Failed to get response from API. Status code: {response.status_code}")

if __name__ == "__main__":
    call_api_and_save_video()