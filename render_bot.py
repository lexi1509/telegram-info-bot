import asyncio
import logging
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.enums import ParseMode
from aiohttp import web

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv('BOT_TOKEN')
if not BOT_TOKEN:
    logger.error("Не задан токен бота!")
    exit(1)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# ---------- КЛАВИАТУРА ----------
def create_main_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="ℹ️ Обо мне", callback_data="about"),
        InlineKeyboardButton(text="📞 Контакты", callback_data="contacts")
    )
    builder.row(
        InlineKeyboardButton(text="📂 Мой GitHub", url="https://github.com/lexi1509")
    )
    builder.row(
        InlineKeyboardButton(text="🌟 Сайт-портфолио", url="https://portfolio-site-r5gq.onrender.com")
    )
    return builder.as_markup()

# ---------- КОМАНДА /start ----------
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    welcome_text = (
        "👋 Привет!\n\n"
        "Меня зовут Любовь. Я начинающий специалист по тестированию.\n"
        "Добро пожаловать в мой бот-визитку!"
    )
    
    await message.answer_photo(
        photo="https://i.ibb.co/DfTpmMgG/avatar.jpg",
        caption=welcome_text,
        reply_markup=create_main_keyboard()
    )

# ---------- КОМАНДА /about ----------
@dp.message(Command("about"))
async def cmd_about(message: types.Message):
    about_text = (
        "ℹ️ **О себе:**\n\n"
        "Я активно учусь и использую современные инструменты, включая искусственный интеллект, чтобы быстрее осваивать новые технологии. Каждый проект я разбираю до деталей — так я расту как специалист."
    )
    await message.answer(about_text, parse_mode=ParseMode.MARKDOWN, reply_markup=create_main_keyboard())

# ---------- КОМАНДА /contacts ----------
@dp.message(Command("contacts"))
async def cmd_contacts(message: types.Message):
    contacts_text = (
        "📞 **Мои контакты:**\n\n"
        "• **Email:** Volsar20141991@yandex.com\n"
        "• **GitHub:** [lexi1509](https://github.com/lexi1509)\n"
        "• **Telegram:** @Alexi1509"
    )
    await message.answer(contacts_text, parse_mode=ParseMode.MARKDOWN, reply_markup=create_main_keyboard())

# ---------- ОБРАБОТЧИК КНОПКИ "Обо мне" ----------
@dp.callback_query(F.data == "about")
async def process_callback_about(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    about_text = (
        "ℹ️ **О себе:**\n\n"
        "Я активно учусь и использую современные инструменты, включая искусственный интеллект, чтобы быстрее осваивать новые технологии. Каждый проект я разбираю до деталей — так я расту как специалист."
    )
    await bot.send_message(
        callback_query.from_user.id,
        about_text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=create_main_keyboard()
    )

# ---------- ОБРАБОТЧИК КНОПКИ "Контакты" ----------
@dp.callback_query(F.data == "contacts")
async def process_callback_contacts(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    contacts_text = (
        "📞 **Мои контакты:**\n\n"
        "• **Email:** Volsar20141991@yandex.com\n"
        "• **GitHub:** [lexi1509](https://github.com/lexi1509)\n"
        "• **Telegram:** @Alexi1509"
    )
    await bot.send_message(
        callback_query.from_user.id,
        contacts_text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=create_main_keyboard()
    )

# ---------- ОБРАБОТЧИК ВСЕГО ОСТАЛЬНОГО ----------
@dp.message()
async def handle_unknown(message: types.Message):
    await message.answer(
        "Я понимаю только команды и кнопки. Используй меню ниже 👇",
        reply_markup=create_main_keyboard()
    )

# ---------- WEBHOOK + HEALTH CHECK (для Render) ----------
async def webhook_handler(request):
    """Получает обновления от Telegram"""
    update = await request.json()
    logger.info(f"Получен webhook: {update.get('update_id')}")
    
    telegram_update = types.Update(**update)
    await dp.feed_update(bot, telegram_update)
    return web.Response(text="OK")

async def health_check(request):
    """Для проверки здоровья Render (обязательно!)"""
    return web.Response(text="OK")

async def set_webhook():
    """Устанавливает webhook на Render URL"""
    webhook_url = os.environ.get("RENDER_EXTERNAL_URL")
    
    if not webhook_url:
        logger.error("RENDER_EXTERNAL_URL не задан")
        return
    
    full_url = f"{webhook_url}/webhook"
    await bot.set_webhook(full_url)
    logger.info(f"Webhook установлен на {full_url}")

async def main():
    """Главная функция запуска"""
    # Устанавливаем webhook
    await set_webhook()
    
    # Создаем aiohttp приложение
    app = web.Application()
    app.router.add_post("/webhook", webhook_handler)
    app.router.add_get("/health", health_check)
    
    port = int(os.environ.get("PORT", 8000))
    logger.info(f"Запуск сервера на порту {port}")
    
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", port)
    
    await site.start()
    logger.info(f"Сервер запущен на порту {port}")
    logger.info("Бот готов к работе через webhook")
    
    # Держим приложение запущенным
    await asyncio.Event().wait()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Бот остановлен")