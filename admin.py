# File: admin.py
"""
Конфігурація та константи для бота
Заповніть BOT_TOKEN і ADMIN_IDS перед використанням.
"""
from typing import List

# Telegram
BOT_TOKEN = "7574202071:AAGshHjJl1Az3r0r1ywCrdl6n8fF1gMA8AQ"
ADMIN_IDS: List[int] = [5444667193]  # Telegram user ids адмінів, отримані через @userinfobot або інші способи

# Site
HOTELS24_BASE = "https://hotels24.ua"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
REQUESTS_HEADERS = {"User-Agent": USER_AGENT}

# Parsing options
PARSE_SLEEP_SECONDS = 1.0  # пауза між запитами, щоб не навантажувати сайт

# Selenium / Booking (якщо будете використовувати автоповнення форм)
# Тут можна вказати шлях до chromedriver або використовувати webdriver-manager у коді
CHROME_DRIVER_PATH = None

# Google Sheets / DB
# Якщо бажаєте зберігати бронювання локально або у Google Sheets,
# додайте тут конфігурацію (необов'язково)