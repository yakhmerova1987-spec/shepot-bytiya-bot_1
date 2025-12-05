import os
from datetime import datetime
from telegram.ext import ApplicationBuilder, MessageHandler, filters
from engine import choose_reply

BOT_TOKEN = os.environ.get("BOT_TOKEN")

async def handle_message(update, context):
    user_text = update.message.text or ""
    reply = choose_reply(user_text, datetime.now())
    await update.message.reply_text(reply)

def main():
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN не найден в переменных окружения")
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
