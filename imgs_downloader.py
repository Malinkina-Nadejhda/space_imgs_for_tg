import urllib.parse
import os.path
import requests


def create_folder(folder):
    os.makedirs(folder, exist_ok=True)
    return folder


def download_imgs(img_url, folder, params):
    response = requests.get(img_url, params=params)
    response.raise_for_status()
    parsed_img_url = urllib.parse.urlparse(img_url)
    img_name = os.path.basename(parsed_img_url.path)
    image_path = os.path.join(folder, f"{img_name}.jpg")
    with open(image_path, "wb") as file:
        file.write(response.content)
