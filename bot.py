import os
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler

from telegram.ext import Updater, MessageHandler, Filters, CommandHandler

from engine import choose_reply


BOT_TOKEN = os.environ.get("BOT_TOKEN")
PORT = int(os.environ.get("PORT", "8000"))  # Render подставит свой порт


def handle_message(update, context):
    """
    Общий обработчик: и для /start, и для любого текста.
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

    # Отдельно обрабатываем команду /start,
    # но тем же самым обработчиком, что и обычный текст
    dp.add_handler(CommandHandler("start", handle_message))

    # Любой текст (включая то, что не команда) → туда же
    dp.add_handler(MessageHandler(Filters.text, handle_message))

    # Запускаем polling в отдельном потоке
    updater.start_polling()

    # Поднимаем простой HTTP-сервер на PORT для Render
    httpd = HTTPServer(("0.0.0.0", PORT), HealthHandler)
    httpd.serve_forever()


if __name__ == "__main__":
    main()
