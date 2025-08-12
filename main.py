# File: main.py
"""
Запуск Telegram бота для бронювань у "Парк Куркулі" (python-telegram-bot v20+ API).
"""
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters

from admin import BOT_TOKEN
from parsing_sites import get_kurkuli_rooms
from keyboard import main_menu_keyboard

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Вітаю! Я бот для бронювання готелю 'Парк Куркулі'. Використайте меню.",
        reply_markup=main_menu_keyboard()
    )

async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    if text.startswith("🔍") or "куркулі" in text.lower():
        await update.message.reply_text("Зачекайте, отримую дані про доступні номери...")
        rooms = get_kurkuli_rooms()

        if not rooms:
            await update.message.reply_text("Наразі немає доступної інформації про номери.")
            return

        for room in rooms:
            msg = f"🏨 {room['name']}\n💰 {room['price'] or 'Ціну уточнюйте'}"
            if room['available_dates']:
                msg += "\n📅 Вільні дати: " + ", ".join(room['available_dates'])
            if room['book_link']:
                msg += f"\n🔗 [Забронювати]({room['book_link']})"

            await update.message.reply_text(msg, parse_mode="Markdown", disable_web_page_preview=True)
        return

    await update.message.reply_text(
        "Введіть 'Парк Куркулі' або скористайтесь меню для пошуку номерів."
    )

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))

    logger.info("Bot started")
    app.run_polling()

if __name__ == '__main__':
    main()