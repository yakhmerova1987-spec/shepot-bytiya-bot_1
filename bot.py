import os
from datetime import datetime

from telegram.ext import Updater, MessageHandler, Filters

from engine import choose_reply


BOT_TOKEN = os.environ.get("BOT_TOKEN")


def handle_message(update, context):
    """
    Обработка любого текстового сообщения.
    """
    user_text = update.message.text or ""
    reply = choose_reply(user_text, now=datetime.now())
    update.message.reply_text(reply)


def main():
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN не найден в переменных окружения")

    # создаём Updater и диспетчер
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    # любой текст (не команда) -> наш обработчик
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # запускаем бота
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
