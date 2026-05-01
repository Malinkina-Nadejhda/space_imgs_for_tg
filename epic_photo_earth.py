import requests
import os
from dotenv import load_dotenv
from imgs_downloader import download_imgs


def get_epic_data(nasa_token, user_date):
    if not user_date:
        url = "https://epic.gsfc.nasa.gov/api/natural"
    else:
        url = f"https://epic.gsfc.nasa.gov/api/natural/date/{user_date}"
    params = {"api_key": nasa_token}
    response = requests.get(url, params=params)
    response.raise_for_status()
    epic_data = response.json()
    return epic_data


def get_epic_imgs_urls(epic_data, nasa_token):
    epic_imgs_urls = []
    for epic in epic_data:
        url = "https://api.nasa.gov/EPIC/archive/natural"
        date = f"{epic.get('date')[0:10]}".replace("-", "/")
        epic_img_url = f"{url}/{date}/png/{epic.get('image')}.png?api_key={nasa_token}"
        epic_imgs_urls.append(epic_img_url)
        epic_imgs_urls = epic_imgs_urls[0:3]
    return epic_imgs_urls


def main():
    load_dotenv()
    user_date = input(
        "Введите дату. Формат гггг-мм-дд. Пример (2026-04-26):\n"
        "Или введите Enter для актуальных фото: "
    )
    try:
        nasa_token = os.getenv("NASA_TOKEN")
        epic_data = get_epic_data(nasa_token, user_date)
        epic_imgs_urls = get_epic_imgs_urls(epic_data, nasa_token)
        download_imgs(epic_imgs_urls)
        print("Скачивание завершено")
    except requests.exceptions.HTTPError:
        print("Ошибка соединения")
    except Exception:
        print("Неизвестная ошибка")


if __name__ == "__main__":
    main()

