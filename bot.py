from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
import requests

BOT_TOKEN = "8499874125:AAFIz6H7DE0BnKcngreUY63UtekqxrmXnlk"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    if "tiktok.com" not in text and "vm.tiktok.com" not in text:
        await update.message.reply_text("❌ Это не ссылка на TikTok.")
        return

    await update.message.reply_text("⏳ Ищу видео через TikWM...")

    try:
        # Запрос к TikWM API
        api_url = f"https://tikwm.com/api/?url={text}"
        response = requests.get(api_url)
        data = response.json()

        if data["code"] != 0:
            await update.message.reply_text("❌ Видео не найдено или API недоступен.")
            return

        video_url = data["data"]["play"]  # Без водяного знака
        title = data["data"]["title"]

        # Отправляем видео
        await update.message.reply_video(video=video_url, caption=title)

    except Exception as e:
        await update.message.reply_text(f"⚠️ Ошибка при скачивании: {e}")

if __name__ == "__main__":
    print("🚀 Бот запускается...")

    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ Бот запущен и ждёт TikTok ссылки.")
    app.run_polling()
