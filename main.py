import os
import requests
import jdatetime
import arabic_reshaper

from bidi.algorithm import get_display
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
MODE = os.getenv("MODE")

FONT = "fonts/Vazirmatn-Bold.ttf"

MORNING = "morning.png"
EVENING = "evening.png"

OUTPUT = "output.png"


def fa(text):
    en = "0123456789"
    fa = "۰۱۲۳۴۵۶۷۸۹"

    for e, f in zip(en, fa):
        text = text.replace(e, f)

    return text


def rtl(text):
    return get_display(
        arabic_reshaper.reshape(text)
    )


def make_image():

    img = Image.open(MORNING)

    draw = ImageDraw.Draw(img)

    font = ImageFont.truetype(FONT,72)

    d = jdatetime.date.today()

    txt = fa(f"{d.year}/{d.month:02}/{d.day:02}")

    txt = rtl(txt)

    draw.text(
        (1450,45),
        txt,
        font=font,
        fill="white"
    )

    img.save(OUTPUT)
def send_photo(photo_path):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"

    with open(photo_path, "rb") as photo:

        response = requests.post(
            url,
            data={
                "chat_id": CHAT_ID
            },
            files={
                "photo": photo
            },
            timeout=60
        )

    print(response.text)

    response.raise_for_status()


if MODE == "morning":

    make_image()

    send_photo(OUTPUT)

elif MODE == "evening":

    send_photo(EVENING)

else:

    raise Exception("MODE is invalid")
