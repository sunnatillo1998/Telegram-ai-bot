import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Салом! Мен Mistral AI ботман.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = update.message.text
    headers = {
        "Authorization": f"Token {REPLICATE_API_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "version": "REPLICATE_MODEL_VERSION",  # Репликейт модели версияси
        "input": {"prompt": prompt}
    }
    response = requests.post(
        "https://api.replicate.com/v1/predictions",
        headers=headers,
        json=data
    )
    result = response.json()
    if 'error' in result:
        await update.message.reply_text(f"Хатолик: {result['error']}")
    else:
        await update.message.reply_text(f"Жавоб: {result['urls']['get']}")

app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.run_polling()
