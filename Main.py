import asyncio
import logging
import requests
import json
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import Message

# --- НАСТРОЙКИ ---
TELEGRAM_TOKEN = "8331550700:AAFA-UEGWxfQLw9FfDFE1J8YaOcKlbNY2To"
OPENROUTER_API_KEY = "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"
DB_FILE = "users.txt" # Файл, где храним ID пользователей

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

# --- ФУНКЦИИ БАЗЫ ДАННЫХ ---
def save_user(user_id):
    if not os.path.exists(DB_FILE):
        open(DB_FILE, 'a').close()
    
    with open(DB_FILE, "r") as f:
        users = f.read().splitlines()
    
    if str(user_id) not in users:
        with open(DB_FILE, "a") as f:
            f.write(f"{user_id}\n")

def get_all_users():
    if not os.path.exists(DB_FILE):
        return []
    with open(DB_FILE, "r") as f:
        return f.read().splitlines()

# --- ЛОГИКА ИИ ---
def get_ai_response(user_text):
    try:
        response = requests.post(
            url="https://openrouter.ai",
            headers={"Authorization": f"Bearer {OPENROUTER_API_KEY}", "Content-Type": "application/json"},
            data=json.dumps({
                "model": "google/gemma-3-4b-it:free",
                "messages": [{"role": "user", "content": user_text}]
            }),
            timeout=20
        )
        return response.json()['choices'][0]['message']['content'] if response.status_code == 200 else "Ошибка API"
    except Exception:
        return "Ошибка связи с ИИ"

# --- ОБРАБОТЧИКИ ---
@dp.message(CommandStart())
async def cmd_start(message: Message):
    save_user(message.from_user.id) # Сохраняем челика в базу
    await message.answer("Я запущен и готов к работе!")

@dp.message()
async def handle_message(message: Message):
    save_user(message.from_user.id) # На всякий случай сохраняем всех пишущих
    await bot.send_chat_action(chat_id=message.chat.id, action="typing")
    answer = get_ai_response(message.text)
    await message.answer(answer)

# --- РАССЫЛКА ПРИ ЗАПУСКЕ ---
async def on_startup():
    users = get_all_users()
    for user_id in users:
        try:
            await bot.send_message(user_id, "🚀 Бот снова в сети и готов отвечать на вопросы!")
        except Exception:
            pass # Если юзер заблокировал бота

async def main():
    # Запускаем рассылку фоном сразу после старта
    asyncio.create_task(on_startup())
    print("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
