# keyboard.py
"""
Кнопки для меню та інлайн.
"""
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

def main_menu_keyboard() -> ReplyKeyboardMarkup:
    kb = [
        [KeyboardButton("🔍 Знайти хостел"), KeyboardButton("📋 Мої бронювання")],
        [KeyboardButton("📞 Зв'язатися з менеджером")]
    ]
    return ReplyKeyboardMarkup(kb, resize_keyboard=True)

def hotel_result_inline(hotel_id: str, hotel_name: str, price: str = None) -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton("Деталі", callback_data=f"details:{hotel_id}")]
    ]
    if price:
        buttons[0].append(InlineKeyboardButton(f"Ціна: {price}", callback_data=f"price:{hotel_id}"))
    buttons.append([InlineKeyboardButton("Забронювати", callback_data=f"book:{hotel_id}")])
    return InlineKeyboardMarkup(buttons)
