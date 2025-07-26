from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from flask import Flask
import threading
import requests
import os
import asyncio

BOT_TOKEN = os.environ.get("BOT_TOKEN", "8499874125:AAFIz6H7DE0BnKcngreUY63UtekqxrmXnlk")

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Бот работает!"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    # TikTok
    if "tiktok.com" in text or "vm.tiktok.com" in text:
        await update.message.reply_text("⏳ TikTok видео загружается...")
        try:
            api_url = f"https://tikwm.com/api/?url={text}"
            response = requests.get(api_url)
            data = response.json()

            if data["code"] != 0:
                await update.message.reply_text("❌ Не удалось скачать видео с TikTok.")
                return

            video_url = data["data"]["play"]
            title = data["data"]["title"]
            await update.message.reply_video(video=video_url, caption=title)

        except Exception as e:
            await update.message.reply_text(f"⚠️ TikTok ошибка: {e}")
        return

    # Instagram
    elif "instagram.com" in text:
        await update.message.reply_text("⏳ Instagram видео загружается...")
        try:
            api_url = f"https://snapinsta.io/api/ajaxSearch"
            headers = {
                "Content-Type": "application/x-www-form-urlencoded",
                "User-Agent": "Mozilla/5.0"
            }
            data = {
                "q": text,
                "lang": "en"
            }

            resp = requests.post(api_url, headers=headers, data=data)
            json_data = resp.json()

            url = json_data["data"]["url"][0]  # первая ссылка на видео
            await update.message.reply_video(video=url, caption="Instagram видео")

        except Exception as e:
            await update.message.reply_text(f"⚠️ Instagram ошибка: {e}")
        return

    # YouTube
    elif "youtube.com" in text or "youtu.be" in text:
        await update.message.reply_text("⏳ YouTube видео загружается...")
        try:
            y2mate_api = "https://ytmate.guru/api/convert"
            payload = {
                "url": text,
                "format": "mp4"
            }

            r = requests.post(y2mate_api, data=payload)
            res = r.json()

            if not res.get("download_url"):
                await update.message.reply_text("❌ Не удалось скачать с YouTube.")
                return

            download_url = res["download_url"]
            title = res.get("title", "YouTube видео")
            await update.message.reply_video(video=download_url, caption=title)

        except Exception as e:
            await update.message.reply_text(f"⚠️ YouTube ошибка: {e}")
        return

    else:
        await update.message.reply_text("❌ Отправь ссылку с TikTok, Instagram или YouTube.")

async def main():
    app_telegram = ApplicationBuilder().token(BOT_TOKEN).build()
    app_telegram.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    await app_telegram.run_polling()

if __name__ == '__main__':
    threading.Thread(target=run_flask).start()
    asyncio.run(main())

    print("✅ Бот запущен и ждёт TikTok ссылки.")
    app.run_polling()
