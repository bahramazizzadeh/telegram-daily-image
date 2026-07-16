import os
import random
import logging
from datetime import datetime

import requests

from config import (
    TELEGRAM_BOT_TOKEN,
    TELEGRAM_CHAT_ID,
    PHOTO_FOLDER
)


# تنظیمات لاگ
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def get_random_photo():
    """
    انتخاب یک عکس از پوشه photos
    """

    extensions = (
        ".jpg",
        ".jpeg",
        ".png",
        ".webp"
    )

    photos = [
        file for file in os.listdir(PHOTO_FOLDER)
        if file.lower().endswith(extensions)
    ]

    if not photos:
        raise Exception("No photos found!")

    return random.choice(photos)


def send_photo_to_telegram(photo_path):
    """
    ارسال عکس به تلگرام
    """

    url = (
        f"https://api.telegram.org/"
        f"bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
    )

    caption = (
        f"📸 Daily Photo\n"
        f"🕒 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )

    with open(photo_path, "rb") as photo:

        response = requests.post(
            url,
            data={
                "chat_id": TELEGRAM_CHAT_ID,
                "caption": caption
            },
            files={
                "photo": photo
            },
            timeout=30
        )

    if response.status_code != 200:
        raise Exception(
            f"Telegram error: {response.text}"
        )

    logging.info(
        "Photo sent successfully!"
    )


def main():

    logging.info(
        "Starting daily telegram photo sender..."
    )

    photo_name = get_random_photo()

    photo_path = os.path.join(
        PHOTO_FOLDER,
        photo_name
    )

    logging.info(
        f"Selected photo: {photo_path}"
    )

    send_photo_to_telegram(photo_path)


if __name__ == "__main__":
    main()
