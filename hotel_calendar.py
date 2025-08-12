# File: calendar.py
"""
Календар для вибору дат — генерація inline клавіатури з можливістю вибрати одну або кілька ночей.
Дати підвантажуються з функції парсингу конкретного готелю.
"""
from datetime import datetime
from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def generate_calendar_keyboard(available_dates, nights_select=False):
    """
    Генерує календар з доступними датами.
    :param available_dates: список дат у форматі "YYYY-MM-DD"
    :param nights_select: якщо True — можна вибрати кілька ночей, інакше тільки одну дату
    """
    if not available_dates:
        return InlineKeyboardMarkup([[InlineKeyboardButton("Немає вільних дат", callback_data="no_dates")]])

    # Сортуємо та групуємо по тижнях
    available_dates_sorted = sorted(
        available_dates,
        key=lambda d: datetime.strptime(d, "%Y-%m-%d")
    )

    buttons = []
    row = []
    for i, d_str in enumerate(available_dates_sorted, start=1):
        d_obj = datetime.strptime(d_str, "%Y-%m-%d")
        text = d_obj.strftime("%d %b")
        cb_data = f"date:{d_str}"
        row.append(InlineKeyboardButton(text, callback_data=cb_data))

        # Розбиваємо на рядки по 7 днів (або якщо залишилось менше)
        if i % 7 == 0 or i == len(available_dates_sorted):
            buttons.append(row)
            row = []

    # Додаткові кнопки
    extra_row = []
    if nights_select:
        extra_row.append(InlineKeyboardButton("✅ Підтвердити вибір", callback_data="confirm_dates"))
    extra_row.append(InlineKeyboardButton("❌ Скасувати", callback_data="cancel"))
    buttons.append(extra_row)

    return InlineKeyboardMarkup(buttons)
