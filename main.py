from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()



import os
import yt_dlp
from pyrogram import Client, filters, enums
from dotenv import load_dotenv

load_dotenv()

app = Client(
    "downloader_bot",
    api_id=os.getenv("API_ID"),
    api_hash=os.getenv("API_HASH"),
    bot_token=os.getenv("BOT_TOKEN")
)


@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text(f"Salom {message.from_user.first_name}! Link yuboring, yuklab beraman! 📥")


@app.on_message(filters.regex(r'http'))
async def download_video(client, message):
    url = message.text
    status_msg = await message.reply_text("Jarayon boshlandi... 🚀")
    file_name = f"video_{message.from_user.id}.mp4"

    try:
        # Fayl yo'lini aniq tekshiramiz
        cookie_path = 'cookies.txt'

        ydl_opts = {
            # Ovoz va video birga bo'lgan eng yaxshi mp4 formatini tanlaymiz
            'format': 'best[ext=mp4]/best',
            'outtmpl': file_name,
            'quiet': True,
            'no_warnings': True,
            'cookiefile': cookie_path if os.path.exists(cookie_path) else None,
            # YouTube-ga o'zimizni haqiqiy brauzerdek ko'rsatamiz
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-us,en;q=0.5',
                'Sec-Fetch-Mode': 'navigate',
            }
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            await status_msg.edit("Video yuklanmoqda... 📥")
            ydl.download([url])

        caption_text = (
            "✅ **@apple_kamron_bot orqali yuklandi**\n\n"
            "📣 **apple_kamron rasmiy telegram kanali:**\n"
            "https://t.me/apple_kamron7"
        )

        await status_msg.edit("Telegramga yuborilmoqda... 📤")
        await message.reply_video(
            video=file_name,
            caption=caption_text,
            parse_mode=enums.ParseMode.MARKDOWN
        )

        await status_msg.delete()
        if os.path.exists(file_name):
            os.remove(file_name)

    except Exception as e:
        error_msg = str(e)
        print(f"TERMINAL XATOSI: {error_msg}")

        if "Sign in to confirm" in error_msg:
            await status_msg.edit(
                "❌ YouTube baribir cookielarni rad etyapti. Iltimos, brauzerda YouTube-ga kirib, videoni 10 soniya ko'ring va yangi cookie oling.")
        else:
            await status_msg.edit(f"Xatolik: {error_msg[:100]}")

        if os.path.exists(file_name):
            os.remove(file_name)


print("Bot qayta ishga tushdi! 🔥")

keep_alive()

app.run()