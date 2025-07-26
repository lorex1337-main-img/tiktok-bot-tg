from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from flask import Flask
import threading
import requests
import os

BOT_TOKEN = os.getenv("BOT_TOKEN", "8499874125:AAFIz6H7DE0BnKcngreUY63UtekqxrmXnlk")

app = Flask(__name__)

@app.route("/")
def home():
    return "✅ Бот работает!"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    if "tiktok.com" in text or "vm.tiktok.com" in text:
        await update.message.reply_text("🎵 TikTok: ищу видео...")
        await handle_tiktok(update, text)

    elif "instagram.com" in text:
        await update.message.reply_text("📸 Instagram: ищу видео...")
        await handle_instagram(update, text)

    elif "youtube.com" in text or "youtu.be" in text:
        await update.message.reply_text("▶️ YouTube: ищу видео...")
        await handle_youtube(update, text)

    else:
        await update.message.reply_text("❌ Поддерживаются TikTok, Instagram и YouTube ссылки.")

async def handle_tiktok(update, link):
    try:
        api_url = f"https://tikwm.com/api/?url={link}"
        response = requests.get(api_url)
        data = response.json()

        if data["code"] != 0:
            await update.message.reply_text("❌ Видео не найдено на TikTok.")
            return

        video_url = data["data"]["play"]
        title = data["data"]["title"]
        await update.message.reply_video(video=video_url, caption=title)

    except Exception as e:
        await update.message.reply_text(f"⚠️ Ошибка TikTok: {e}")

async def handle_instagram(update, link):
    try:
        api_url = f"https://snapinsta.app/api/ajaxSearch"
        headers = {
            "x-requested-with": "XMLHttpRequest",
            "user-agent": "Mozilla/5.0"
        }
        data = {"q": link}
        res = requests.post(api_url, headers=headers, data=data)
        video_url = res.text.split('href="')[1].split('"')[0]

        await update.message.reply_video(video=video_url, caption="📸 Видео с Instagram")

    except Exception as e:
        await update.message.reply_text(f"⚠️ Ошибка Instagram: {e}")

async def handle_youtube(update, link):
    try:
        api_url = f"https://api.vevioz.com/api/widgetv2?url={link}"
        res = requests.get(api_url)
        json_data = res.json()
        video_url = json_data['data'][0]['url']

        await update.message.reply_video(video=video_url, caption="▶️ Видео с YouTube")

    except Exception as e:
        await update.message.reply_text(f"⚠️ Ошибка YouTube: {e}")

def run_telegram():
    app_telegram = ApplicationBuilder().token(BOT_TOKEN).build()
    app_telegram.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app_telegram.run_polling()

def run_flask():
    app.run(host="0.0.0.0", port=8080)

if __name__ == "main":
    threading.Thread(target=run_flask).start()
    run_telegram()
