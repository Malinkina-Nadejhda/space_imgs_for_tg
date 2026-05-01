import os
import telegram
from dotenv import load_dotenv
import time
import random


def send_img(bot, tg_chat_id, user_input):
    img_path = user_input
    try:
        with open(img_path, 'rb') as photo:
            bot.send_photo(chat_id=tg_chat_id, photo=photo)
    except Exception:
        print("Ошибка при отправке")


def send_random_imgs(bot, tg_chat_id, interval):
    imgs_folder = input(r"Введите путь к папке: ")
    imgs = os.listdir(imgs_folder)
    while True:
        random.shuffle(imgs)
        for img in imgs:
            img_path = os.path.join(imgs_folder, img)
            try:
                with open(img_path, 'rb') as photo:
                    bot.send_photo(chat_id=tg_chat_id, photo=photo)
                    time.sleep(interval)
            except Exception:
                print("Ошибка при отправке")


def main():
    user_input = input(
        "Введите путь к изображению, \n"
        "или нажмите Enter, для запуска\n"
        "отложенных публикаций: "
    )
    load_dotenv()
    tg_token = os.getenv("TELEGRAM_TOKEN")
    tg_chat_id = os.getenv("TG_CHAT_ID")
    interval = int(os.getenv("PUBLIC_INTERVAL", 14400))
    bot = telegram.Bot(token=tg_token)
    if not user_input:
        send_random_imgs(bot, tg_chat_id, interval)
    else:
        send_img(bot,tg_chat_id, user_input)


if __name__ == "__main__":
    main()

