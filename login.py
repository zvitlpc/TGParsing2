# File: login.py
"""
Модуль бронювання.
Доступні два підходи:
 - Генерувати посилання на сторінку бронювання і переадресовувати користувача (рекомендований)
 - Автоматизувати форму (Selenium) — більш крихкий, потребує налаштування браузера

У цьому модулі реалізована обгортка для обох підходів. Використовуйте book_via_link у продакшені.
"""
from typing import Dict
import logging

logger = logging.getLogger(__name__)


def book_via_link(book_link: str, user_data: Dict) -> Dict:
    """
    Просто повертає посилання для завершення бронювання користувачем на сайті.
    Можна додатково вбудовувати UTM-мітки або дані контакту в query params.
    """
    # Тут можна додати параметри UTM або contact, якщо сайт підтримує передачу через GET-параметри
    return {"status": "need_user_action", "book_link": book_link}


# Приклад автозаповнення через Selenium (необов'язково):
def book_via_selenium(book_link: str, user_data: Dict, headless: bool = True) -> Dict:
    """
    Автоматичне заповнення форми бронювання через Selenium.
    НЕ гарантується робота для кожного сайту — потрібно налаштовувати селектори.
    """
    try:
        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from selenium.webdriver.chrome.options import Options
        from webdriver_manager.chrome import ChromeDriverManager
    except Exception as e:
        logger.exception("Selenium or webdriver-manager not installed")
        return {"status": "error", "error": str(e)}

    opts = Options()
    if headless:
        opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=opts)
    try:
        driver.get(book_link)
        # Пример заповнення полів — замінити селектори на реальні
        # driver.find_element(By.NAME, "guest_name").send_keys(user_data.get("name"))
        # driver.find_element(By.NAME, "phone").send_keys(user_data.get("phone"))
        # driver.find_element(By.CSS_SELECTOR, "button.submit").click()
        return {"status": "ok", "message": "attempted"}
    except Exception as e:
        logger.exception("Selenium booking failed")
        return {"status": "error", "error": str(e)}
    finally:
        driver.quit()