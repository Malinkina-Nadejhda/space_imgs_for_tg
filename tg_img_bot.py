import os
import telegram
import time
import random
import argparse
from dotenv import load_dotenv
from telegram.error import NetworkError, TimedOut, TelegramError, InvalidToken


def send_img(bot, tg_chat_id, path):
    with open(path, 'rb') as photo:
        bot.send_photo(chat_id=tg_chat_id, photo=photo)


def main():
    load_dotenv()
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode",
        choices=["img", "auto"],
        default="auto",
        help="img - запостить фото,\n"
             "auto - автоматические публикации"
    )
    parser.add_argument(
        "--path",
        type=str,
        required=True,
        help="Путь к папке\n"
             "или изображению"
    )
    args = parser.parse_args()
    interval = int(os.getenv("PUBLIC_INTERVAL", 14400))
    delay = 10
    try:
        tg_token = os.environ["TELEGRAM_TOKEN"]
        tg_chat_id = os.environ["TG_CHAT_ID"]
    except KeyError:
        print("Ошибка, не найдена переменные 'TELEGRAM_TOKEN' или"
              "'TG_CHAT_ID' в .env файле!")
        return
    try:
        bot = telegram.Bot(token=tg_token)
        bot.get_me()
    except InvalidToken:
        print("Невалидный токен бота, "
              "Проверьте файл .env")
        return
    try:
        bot.send_chat_action(chat_id=tg_chat_id, action=telegram.ChatAction.TYPING)
    except TelegramError:
        print("Отсутсвует id чата, "
              "Проверьте файл .env")
        return

    while True:
        try:
            if args.mode == "auto":
                imgs = os.listdir(args.path)
                while True:
                    random.shuffle(imgs)
                    for img in imgs:
                        img_path = os.path.join(args.path, img)
                        send_img(bot, tg_chat_id, img_path)
                        time.sleep(interval)
            else:
                send_img(bot, tg_chat_id, args.path)
            break
        except (NetworkError, TimedOut):
            print("Ошибка соединения")
            print(f"Повторное соединение через {delay} секунд")
            time.sleep(delay)
        except FileNotFoundError:
            print("Не найден файл или директория")
            break
        except TypeError:
            print("Неверный тип файла")
            break


if __name__ == "__main__":
    main()


