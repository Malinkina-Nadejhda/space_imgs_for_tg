import urllib.parse
import os.path
import requests


def download_imgs(imgs_urls):
    folder = "Images"
    os.makedirs(folder, exist_ok=True)

    for img_number, img_url in enumerate(imgs_urls):
        response = requests.get(img_url)
        response.raise_for_status()
        parsed_img_url = urllib.parse.urlparse(img_url)
        img_name = os.path.basename(parsed_img_url.path)
        image_path = os.path.join(folder, f"{img_number}_spacex_{img_name}.jpg")
        with open(image_path, "wb") as file:
            file.write(response.content)