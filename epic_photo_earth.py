import requests
import os
import configargparse
from dotenv import load_dotenv
from imgs_downloader import download_imgs, create_folder
from datetime import datetime


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


def get_epic_imgs_urls(epic_data, count):
    epic_imgs_urls = []
    for epic in epic_data[:count]:
        url = "https://api.nasa.gov/EPIC/archive/natural"
        date_str = epic["date"]
        date_obj = datetime.fromisoformat(date_str)
        date = date_obj.strftime("%Y/%m/%d")
        epic_img_url = f"{url}/{date}/png/{epic["image"]}.png"
        epic_imgs_urls.append(epic_img_url)
    return epic_imgs_urls


def main():
    load_dotenv()
    parser = configargparse.ArgumentParser()
    parser.add_argument(
        "--mode",
        choices=["last", "date"],
        default="last",
        help="last - самые свежие фото,\n"
             "date - фото с заданной даты,\n"
             "default - last"
    )
    parser.add_argument(
        "--date",
        type=str,
        help="Нужен для --mode date.\n"
             "Дата в формате ГГГГ-ММ-ДД.\n"
             "Пример ввода: --mode date --date 2026-04-26"
    )
    parser.add_argument(
        "--folder",
        type=str,
        env_var="EPIC_FOLDER",
        default="Images",
        help="Имя папки\Путь к папке"
    )
    args = parser.parse_args()
    try:
        nasa_token = os.environ["NASA_TOKEN"]
    except KeyError:
        print("Не найдена переменная 'NASA_TOKEN'"
              "в .env файле")
        return

    try:
        count = int(os.getenv("QUANTITY_EPIC", 5))
        if args.mode == "date":
            epic_data = get_epic_data(nasa_token, args.date)
        else:
            epic_data = get_epic_data(nasa_token, None)
        epic_imgs_urls = get_epic_imgs_urls(epic_data, count)
        folder = create_folder(args.folder)
        for epic_img_url in epic_imgs_urls:
            download_imgs(epic_img_url, folder, nasa_token)
        print("Скачивание завершено")
    except requests.exceptions.HTTPError as err:
        if err.response.status_code == 403:
            print("Невалидный токен NASA API.")
    except requests.exceptions.ConnectionError:
        print("Ошибка соединения. Проверьте подключение")


if __name__ == "__main__":
    main()
