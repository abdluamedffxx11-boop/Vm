import logging
from aiogram import Bot, Dispatcher, executor, types
import os

# 1. ضع توكن البوت الخاص بك هنا
API_TOKEN = 'YOUR_BOT_TOKEN_HERE' 

# 2. الـ ID الخاص بك (المتحكم في البوت)
ADMIN_ID = 8369014219 

# إعداد السجلات لمتابعة عمل البوت
logging.basicConfig(level=logging.INFO)

# إنشاء كائن البوت والموزع
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# وظيفة لحفظ الـ ID في ملف نصي
def add_user(user_id):
    file_path = 'users.txt'
    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            f.write('')
    
    with open(file_path, 'r') as f:
        users = f.read().splitlines()
    
    if str(user_id) not in users:
        with open(file_path, 'a') as f:
            f.write(f"{user_id}\n")

# أمر البدء
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    add_user(message.from_user.id)
    await message.answer("أهلاً بك يا دراكون! أرسل لي رابط الفيديو وسأقوم بتحميله لك.")

# أمر إحصائيات للمطور (الأدمن)
@dp.message_handler(commands=['stats'])
async def get_stats(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        if os.path.exists('users.txt'):
            with open('users.txt', 'r') as f:
                count = len(f.read().splitlines())
            await message.answer(f"عدد المستخدمين الكلي: {count}")
        else:
            await message.answer("لا يوجد مستخدمون بعد.")
    else:
        await message.answer("عذراً، هذا الأمر مخصص للمطور فقط.")

# معالجة الروابط
@dp.message_handler()
async def download_video(message: types.Message):
    if "http" in message.text:
        await message.answer("⏳ جاري المعالجة والتحميل...")
        # هنا ستضع كود التحميل (yt-dlp) لاحقاً
    else:
        await message.answer("يرجى إرسال رابط صحيح.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
