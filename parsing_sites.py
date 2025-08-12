# parsing_sites.py
"""
Парсер готелю "Парк Куркулі" з сайту Hotels24.ua.
Витягує назви номерів, ціни та посилання на сторінку бронювання,
завантажуючи дані напряму з URL.
"""
import time
import requests
from bs4 import BeautifulSoup
from typing import List, Dict
import re

# Константи для запитів
REQUESTS_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}
PARSE_SLEEP_SECONDS = 1  # Невелика затримка, щоб не перевантажувати сайт
KURKULI_URL = "https://hotels24.ua/uk/Tulchyn/Park-Hotel-Kurkuli-16379.html"


def _get_soup(url: str) -> BeautifulSoup | None:
    """
    Виконує GET-запит до вказаного URL, щоб отримати HTML-вміст.
    Повертає об'єкт BeautifulSoup для парсингу.
    """
    try:
        # Робимо запит до сайту, імітуючи браузер
        r = requests.get(url, headers=REQUESTS_HEADERS, timeout=15)
        # Перевіряємо, чи успішний запит (код 200)
        r.raise_for_status()
        return BeautifulSoup(r.text, "html.parser")
    except requests.RequestException as e:
        print(f"Помилка при завантаженні сторінки {url}: {e}")
        return None


def get_kurkuli_rooms() -> List[Dict]:
    """
    Парсить сторінку готелю з сайту Hotels24.ua, щоб отримати інформацію про номери.
    """
    print(f"🔎 Починаю парсинг сторінки: {KURKULI_URL}")
    soup = _get_soup(KURKULI_URL)
    if soup is None:
        return []  # Повертаємо порожній список, якщо не вдалося завантажити сторінку

    # Затримка між запитами є гарною практикою
    time.sleep(PARSE_SLEEP_SECONDS)

    rooms = []
    # Використовуємо ті ж самі, вже перевірені селектори
    room_blocks = soup.select("table.room-table")

    if not room_blocks:
        print("⚠️ Не знайдено блоків з номерами за селектором 'table.room-table'. Можливо, структура сайту змінилася.")
        return []

    for block in room_blocks:
        name_tag = block.select_one("caption")
        name = name_tag.get_text(strip=True) if name_tag else "Назву не знайдено"

        price_tag = block.select_one(".price")
        price = price_tag.get_text(strip=True) if price_tag else None
        if price:
            price = re.sub(r"[^\d]", "", price)

        book_link = KURKULI_URL
        available_dates = []

        if name and price:
            rooms.append({
                "name": name,
                "price": price,
                "book_link": book_link,
                "available_dates": available_dates
            })

    return rooms


# Приклад виклику функції
if __name__ == '__main__':
    kurkuli_rooms_data = get_kurkuli_rooms()
    if kurkuli_rooms_data:
        print("\n✅ Успішно зібрано дані. Знайдено наступні номери:")
        for room in kurkuli_rooms_data:
            print(f"\n- Назва: **{room['name']}**")
            print(f"  Ціна: {room['price']} грн")
            print(f"  Сторінка для бронювання: {room['book_link']}")
            print("-" * 25)
    else:
        print("\n❌ Не вдалося отримати дані про номери з сайту.")