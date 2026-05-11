import requests
import urllib.parse
import os.path
import os
from dotenv import load_dotenv
from imgs_downloader import download_imgs, create_folder
import configargparse


def get_apod_urls_collection(nasa_token, count):
    nasa_apod_url = "https://api.nasa.gov/planetary/apod"
    params = {"api_key": nasa_token,
              "count": count}
    encoded_params = urllib.parse.urlencode(params)
    response = requests.get(nasa_apod_url, params=encoded_params)
    response.raise_for_status()
    apod_collection = response.json()
    apod_urls_collection = []

    for apod in apod_collection:
        if apod["media_type"] == "image":
            apod_urls_collection.append(apod["url"])
    return apod_urls_collection


def get_apod_day_url(nasa_token):
    nasa_apod_url = "https://api.nasa.gov/planetary/apod"
    params = {"api_key": nasa_token, }
    encoded_params = urllib.parse.urlencode(params)
    response = requests.get(nasa_apod_url, params=encoded_params)
    response.raise_for_status()
    apod_day_url = response.json().get("url")
    apod_day_url = [apod_day_url]
    return apod_day_url


def get_jpg_urls(apod_urls):
    imgs_urls_collection = []
    for url in apod_urls:
        parsed_url = urllib.parse.urlparse(url)
        file_path = parsed_url.path
        file_name = os.path.split(file_path)[1]
        type_file = os.path.splitext(file_name)[1]
        if type_file == ".jpg":
            imgs_urls_collection.append(url)
    return imgs_urls_collection


def main():
    load_dotenv()
    parser = configargparse.ArgumentParser()
    parser.add_argument(
        "--mode",
        choices=["collection", "day"],
        default="day",
        help="collection - коллекция,\n"
             "day - фото дня,\n"
             "default - day"
    )
    parser.add_argument(
        "--folder",
        type=str,
        env_var="APOD_FOLDER",
        default="Images",
        help="Имя папки\Путь к папке"
    )
    args = parser.parse_args()
    nasa_token = os.environ["NASA_TOKEN"]
    try:
        if args.mode == "collection":
            count = int(os.getenv("QUANTITY_APOD", 5))
            apod_urls = get_apod_urls_collection(nasa_token, count)
            apod_imgs_urls = get_jpg_urls(apod_urls)
            folder = create_folder(args.folder)
            for img_url in apod_imgs_urls:
                download_imgs(img_url, folder, None)
            print("Скачивание завершено")
        else:
            apod_day_url = get_apod_day_url(nasa_token)
            day_img_url = get_jpg_urls(apod_day_url)
            if not day_img_url:
                print("Сегодня нет фото от Nasa")
            else:
                folder = create_folder(args.folder)
                download_imgs(day_img_url, folder, None)
                print("Скачивание завершено")
    except requests.exceptions.HTTPError:
        print("Ошибка соединения")
    except Exception:
        print("Неизвестная ошибка")


if __name__ == "__main__":
    main()
