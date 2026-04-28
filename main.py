from flask import Flask
from threading import Thread
import os
import yt_dlp
from pyrogram import Client, filters, enums
from dotenv import load_dotenv

# 1. RENDER UCHUN SOXTA VEB-SERVER (PORT OCHISH)
server = Flask('')

@server.route('/')
def home():
    return "Bot is alive! 🚀"

def run_server():
    # Render avtomatik beradigan PORT-ni olamiz yoki 8080 ishlatamiz
    port = int(os.environ.get("PORT", 8080))
    server.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run_server)
    t.daemon = True # Bot o'chganda bu ham o'chishi uchun
    t.start()

# 2. BOTNI SOZLASH
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
        cookie_path = 'cookies.txt'
        ydl_opts = {
            'format': 'best[ext=mp4]/best',
            'outtmpl': file_name,
            'quiet': True,
            'no_warnings': True,
            'cookiefile': cookie_path if os.path.exists(cookie_path) else None,
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
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
        print(f"XATOLIK: {str(e)}")
        await status_msg.edit(f"Xatolik yuz berdi. (Instagram story bo'lsa login talab qilinishi mumkin)")
        if os.path.exists(file_name):
            os.remove(file_name)

# 3. ASOSIY ISHGA TUSHIRISH QISMI
if __name__ == "__main__":
    print("Server port ochmoqda...")
    keep_alive() # Flask-ni fonda ishga tushiramiz
    print("Bot ishga tushdi! 🔥")
    app.run() # Botni ishga tushiramiz