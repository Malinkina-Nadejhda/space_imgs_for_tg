import os
import telegram
import time
import random
import argparse
from dotenv import load_dotenv
from telegram.error import NetworkError, TimedOut, TelegramError


def send_img(bot, tg_chat_id, path):
    with open(path, 'rb') as photo:
        bot.send_photo(chat_id=tg_chat_id, photo=photo)


def send_random_imgs(bot, tg_chat_id, path, interval):
    imgs_folder = path
    imgs = os.listdir(imgs_folder)
    while True:
        random.shuffle(imgs)
        for img in imgs:
            img_path = os.path.join(imgs_folder, img)
            with open(img_path, 'rb') as photo:
                bot.send_photo(chat_id=tg_chat_id, photo=photo)
                time.sleep(interval)


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
    tg_token = os.environ["TELEGRAM_TOKEN"]
    tg_chat_id = os.environ["TG_CHAT_ID"]
    interval = int(os.getenv("PUBLIC_INTERVAL", 14400))
    bot = telegram.Bot(token=tg_token)
    delay = 10
    while True:
        try:
            if args.mode == "auto":
                send_random_imgs(bot, tg_chat_id, args.path, interval)
            else:
                send_img(bot, tg_chat_id, args.path)
            break
        except (NetworkError, TimedOut, TelegramError):
            print("Ошибка соединения")
            print(f"Повторное соединение через {delay} секунд")
            time.sleep(delay)
        except KeyError:
            print("Ошибка, не найден токен авторизации!")
            break
        except FileNotFoundError:
            print("Не найден файл или директория")
            break
        except TypeError:
            print("Неверный тип файла")
            break
        except Exception as err:
            print(f"Ошибка {err}")
            break


if __name__ == "__main__":
    main()

