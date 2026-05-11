import requests
import configargparse
from imgs_downloader import download_imgs, create_folder
from dotenv import load_dotenv


def get_laters_launch():
    url = f"https://api.spacexdata.com/v5/launches"
    response = requests.get(url)
    response.raise_for_status()
    launches = response.json()

    for launch in reversed(launches):
        flickr_photos = launch.get("links").get("flickr").get("original")
        if flickr_photos:
            latest_launch = flickr_photos
            return latest_launch


def get_launch(user_input):
    url = f"https://api.spacexdata.com/v5/launches/{user_input}"
    response = requests.get(url)
    response.raise_for_status()
    launch = response.json().get("links").get("flickr").get("original")
    return launch


def main():
    load_dotenv()
    parser = configargparse.ArgumentParser()
    parser.add_argument(
        "--mode",
        choices=["last", "id"],
        default="last",
        help="last - последний запуск,\n"
             "id - id запуска,\n"
             "default - last"
    )
    parser.add_argument(
        "--id",
        type=str,
        help="Нужен для --mode id.\n"
             "Пример: --mode id --id 5eb87d46ffd86e000604b388"
    )
    parser.add_argument(
        "--folder",
        type=str,
        env_var="FETCH_FOLDER",
        default="Images",
        help="Имя папки\Путь к папке"
    )
    args = parser.parse_args()

    try:
        if args.mode == "last":
            launch = get_laters_launch()
            folder = create_folder(args.folder)
            for img_url in launch:
                download_imgs(img_url, folder, None)
            print("Скачивание завершено")
        else:
            launch = get_launch(args.id)
            folder = create_folder(args.folder)
            for img_url in launch:
                download_imgs(img_url, folder, None)
            print("Скачивание завершено")
    except requests.exceptions.HTTPError:
        print("Ошибка соединения")
    except Exception:
        print("Неизвестная ошибка")


if __name__ == "__main__":
    main()
