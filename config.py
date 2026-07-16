import os


# توکن ربات تلگرام
TELEGRAM_BOT_TOKEN = os.getenv(
    "TELEGRAM_BOT_TOKEN"
)


# آیدی چت، گروه یا کانالی که عکس باید ارسال شود
TELEGRAM_CHAT_ID = os.getenv(
    "TELEGRAM_CHAT_ID"
)


# مسیر پوشه عکس‌ها
PHOTO_FOLDER = os.getenv(
    "PHOTO_FOLDER",
    "photos"
)


# بررسی تنظیمات ضروری

if not TELEGRAM_BOT_TOKEN:
    raise ValueError(
        "TELEGRAM_BOT_TOKEN is missing!"
    )


if not TELEGRAM_CHAT_ID:
    raise ValueError(
        "TELEGRAM_CHAT_ID is missing!"
    )
