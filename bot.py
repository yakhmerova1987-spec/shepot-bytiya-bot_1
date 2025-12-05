import os
from datetime import datetime

from telegram.ext import Updater, MessageHandler, Filters

from engine import choose_reply


BOT_TOKEN = os.environ.get("BOT_TOKEN")
APP_URL = os.environ.get("APP_URL")  # https://имя-сервиса.onrender.com
PORT = int(os.environ.get("PORT", "8000"))  # Render сам подставит PORT


def handle_message(update, context):
    """
    Обработка любого текстового сообщения.
    """
    if not update.message:
        return

    user_text = update.message.text or ""
    reply = choose_reply(user_text, now=datetime.now())
    update.message.reply_text(reply)


def main():
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN не найден в переменных окружения")
    if not APP_URL:
        raise RuntimeError("APP_URL не найден в переменных окружения")

    # создаём Updater и диспетчер
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    # любой текст (кроме команд) -> наш обработчик
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # запускаем webhook-сервер
    updater.start_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=BOT_TOKEN,  # путь для Telegram
    )

    webhook_url = APP_URL.rstrip("/") + "/" + BOT_TOKEN
    updater.bot.set_webhook(webhook_url)

    updater.idle()


if __name__ == "__main__":
    main()
