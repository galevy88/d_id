import requests

def download_video(url, file_name):
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        with open(file_name, 'wb') as file:
            file.write(response.content)
        return f"Video downloaded as {file_name}"
    else:
        return "Failed to download the video"