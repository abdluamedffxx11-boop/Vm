import os
import asyncio
import yt_dlp
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import FSInputFile
from dotenv import load_dotenv

# تحميل التوكن
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# إنشاء مجلد التحميل إذا لم يكن موجوداً
if not os.path.exists("downloads"):
    os.makedirs("downloads")

async def download_video(url):
    # إعدادات التحميل (أفضل جودة فيديو)
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'downloads/%(id)s.%(ext)s',
        'noplaylist': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return f"downloads/{info['id']}.{info['ext']}"

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("أهلاً دراكون! أرسل لي رابط فيديو وسأقوم بتحميله لك فوراً.")

@dp.message(F.text.contains("http"))
async def handle_video(message: types.Message):
    msg = await message.answer("⏳ جاري التحميل، يرجى الانتظار...")
    try:
        file_path = await download_video(message.text)
        await message.answer_video(FSInputFile(file_path))
        await msg.delete()
        
        # الحذف بعد الإرسال
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        await msg.edit_text(f"❌ حدث خطأ أثناء التحميل: {e}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

