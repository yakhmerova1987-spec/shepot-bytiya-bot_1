import os
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler

from telegram.ext import Updater, MessageHandler, Filters

from engine import choose_reply


BOT_TOKEN = os.environ.get("BOT_TOKEN")
PORT = int(os.environ.get("PORT", "8000"))  # Render подставит свой порт


def handle_message(update, context):
    """
    Обработка любого текстового сообщения.
    """
    if not update.message:
        return

    user_text = update.message.text or ""
    reply = choose_reply(user_text, now=datetime.now())
    update.message.reply_text(reply)


class HealthHandler(BaseHTTPRequestHandler):
    """
    Простейший HTTP-сервер, чтобы Render видел открытый порт.
    """
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write("shepot bytiya is breathing".encode("utf-8"))


def main():
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN не найден в переменных окружения")

    # Настраиваем Telegram-бота (long polling)
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # Запускаем polling (бот в отдельном потоке)
    updater.start_polling()

    # Поднимаем простой HTTP-сервер на PORT для Render,
    # чтобы он видел открытый порт и не ругался
    httpd = HTTPServer(("0.0.0.0", PORT), HealthHandler)
    httpd.serve_forever()


if __name__ == "__main__":
    main()
