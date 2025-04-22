import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = os.getenv("BOT_TOKEN")
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я ИИ-бот. Задай мне вопрос.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text

    headers = {
        "Authorization": f"Token {REPLICATE_API_TOKEN}",
        "Content-Type": "application/json",
    }
    json_data = {
        "version": "a7c8cd352bc3406e8e4f79f6b5ef358e4f85cdd0b9b4d9452b4f5a45d125d981",
        "input": {"prompt": user_input}
    }
    response = requests.post("https://api.replicate.com/v1/predictions", headers=headers, json=json_data)
    
    if response.status_code == 201:
        prediction = response.json()
        output_url = prediction["urls"]["get"]
        await update.message.reply_text("Думаю...")
        
        import time
        for _ in range(10):
            result = requests.get(output_url, headers=headers).json()
            if result.get("status") == "succeeded":
                await update.message.reply_text(result["output"])
                return
            time.sleep(1)
        await update.message.reply_text("Ответ не получен вовремя.")
    else:
        await update.message.reply_text("Произошла ошибка при подключении к ИИ.")

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
