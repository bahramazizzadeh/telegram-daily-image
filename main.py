import os
import requests
import jdatetime

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import arabic_reshaper
from bidi.algorithm import get_display


BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

FONT = "fonts/Vazirmatn-Bold.ttf"

MORNING_IMAGE = "morning.png"
EVENING_IMAGE = "evening.png"

OUTPUT_IMAGE = "today.png"


def persian_digits(text):

    nums = "0123456789"
    persian = "۰۱۲۳۴۵۶۷۸۹"

    for a, b in zip(nums, persian):
        text = text.replace(a, b)

    return text


def today():

    d = jdatetime.date.today()

    txt = f"{d.year}/{d.month:02}/{d.day:02}"

    return persian_digits(txt)


def rtl(text):

    return get_display(
        arabic_reshaper.reshape(text)
    )


def draw_date():

    image = Image.open(MORNING_IMAGE)

    draw = ImageDraw.Draw(image)

    font = ImageFont.truetype(FONT,72)

    text = rtl(today())

    bbox = draw.textbbox((0,0),text,font=font)

    w = bbox[2]-bbox[0]
    h = bbox[3]-bbox[1]

    x = 1520
    y = 60

    draw.text(
        (x-w//2,y),
        text,
        fill="white",
        font=font
    )

    image.save(OUTPUT_IMAGE)

def send_photo(filename):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"

    with open(filename, "rb") as photo:

        requests.post(
            url,
            data={
                "chat_id": CHAT_ID
            },
            files={
                "photo": photo
            }
        )


def morning():

    draw_date()

    send_photo(OUTPUT_IMAGE)


def evening():

    send_photo(EVENING_IMAGE)


if __name__ == "__main__":

    mode = os.getenv("MODE")

    if mode == "morning":

        morning()

    else:

        evening()   
