import asyncio
import os
from aiogram import Bot, Dispatcher, F, types
from aiogram.enums import ParseMode
from aiogram.types import BotCommand, ReplyKeyboardMarkup, KeyboardButton
from filters import filter_lots
from parser import fetch_lots

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")

bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.MARKDOWN)
dp = Dispatcher()

# --- Reply-кнопки ---
reply_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="🔍 Найти участки")]],
    resize_keyboard=True
)

@dp.message(F.text == "/start")
async def start(message: types.Message):
    await message.answer(
        "👋 Привет! Я ищу для тебя участки ИЖС и СНТ в Новосибирске и Омске.\nНажми кнопку ниже, чтобы запустить поиск вручную.",
        reply_markup=reply_keyboard
    )

@dp.message(F.text == "🔍 Найти участки")
async def manual_search(message: types.Message):
    await message.answer("⏳ Ищу актуальные лоты...")
    lots = fetch_lots()
    filtered = filter_lots(lots)
    if not filtered:
        await message.answer("⚠️ Участки не найдены.")
        return
    for lot in filtered:
        text = f"📍 *{lot['title']}*\nЦена: {lot['price']} ₽\n[Смотреть]({lot['url']})"
        await message.answer(text)

async def daily_job():
    lots = fetch_lots()
    filtered = filter_lots(lots)
    for lot in filtered:
        text = f"📍 *{lot['title']}*\nЦена: {lot['price']} ₽\n[Смотреть]({lot['url']})"
        await bot.send_message(chat_id=ADMIN_ID, text=text)

async def set_bot_commands():
    await bot.set_my_commands([
        BotCommand(command="start", description="Запуск бота"),
        BotCommand(command="restart", description="Перезапуск бота")
    ])

async def main():
    await set_bot_commands()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
