import requests
from imgs_downloader import download_imgs


def get_laters_launch():
    url = f"https://api.spacexdata.com/v5/launches"
    response = requests.get(url)
    response.raise_for_status()
    launches = response.json()

    for launch in reversed(launches):
        flickr_photos = launch.get("links").get("flickr").get("original")
        if flickr_photos:
            latest_launch = launch.get("links").get("flickr").get("original")
            return latest_launch


def get_launch(user_input):
    url = f"https://api.spacexdata.com/v5/launches/{user_input}"
    response = requests.get(url)
    response.raise_for_status()
    launch = response.json().get("links").get("flickr").get("original")
    return launch


def main():
    user_input = input(
        "Введите id запуска, \n"
        "или нажмите Enter для загрузки фото с последнего запуска: "
    )
    try:
        if not user_input:
            launch = get_laters_launch()
            download_imgs(launch)
            print("Скачивание завершено")
        else:
            launch = get_launch(user_input)
            download_imgs(launch)
            print("Скачивание завершено")
    except requests.exceptions.HTTPError:
        print("Ошибка соединения")
    except Exception:
        print("Неизвестная ошибка")


if __name__ == "__main__":
    main()

