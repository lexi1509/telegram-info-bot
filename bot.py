import asyncio
import logging
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.enums import ParseMode

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv('BOT_TOKEN')
if not BOT_TOKEN:
    logger.error("Не задан токен бота! Создайте файл .env с BOT_TOKEN=ваш_токен")
    exit(1)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

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
        InlineKeyboardButton(text="🌟 Сайт-портфолио", url="http://127.0.0.1:5003")
    )
    return builder.as_markup()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    logger.info(f"Пользователь {message.from_user.first_name} (id: {message.from_user.id}) запустил бота")
    
    welcome_text = (
        "👋 Привет!\n\n"
        "Меня зовут Любовь. Я начинающий специалист по тестированию.\n"
        "Добро пожаловать в мой бот-визитку! Здесь ты можешь узнать обо мне, моих проектах и контактах 👇"
    )
    
    try:
        photo = FSInputFile("avatar.jpg")
        await message.answer_photo(
            photo=photo,
            caption=welcome_text,
            reply_markup=create_main_keyboard()
        )
    except FileNotFoundError:
        await message.answer(
            welcome_text,
            reply_markup=create_main_keyboard()
        )

@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    help_text = (
        "📋 **Доступные команды:**\n\n"
        "/start - Начать работу с ботом\n"
        "/help - Показать эту справку\n"
        "/about - Информация обо мне\n"
        "/contacts - Мои контакты\n"
        "/site - Ссылка на мой сайт-портфолио\n\n"
        "Также можно использовать кнопки меню для навигации."
    )
    await message.answer(help_text, parse_mode=ParseMode.MARKDOWN)

@dp.message(Command("about"))
async def cmd_about(message: types.Message):
    about_text = (
        "ℹ️ **Обо мне:**\n\n"
        "Я начинающий специалист по тестированию, живу и работаю в Саратове. Мой путь в IT начался с изучения Python и желания понять, как создаются и совершенствуются цифровые продукты.\n\n"
        "Для меня тестирование — это не просто рутинная проверка, а увлекательный процесс исследования продукта. Я использую современные инструменты, такие как MySQL для работы с базами данных, Flask для понимания backend-логики и Telegram API для создания pet-проектов. Эти проекты помогают мне не только прокачивать технические навыки, но и видеть полную картину создания продукта — от идеи до реализации.\n\n"
        "Мой подход к работе строится на трёх китах: внимательность к деталям, ответственность за результат и постоянное стремление к развитию. Я убеждена, что хороший тестировщик — это не просто тот, кто находит баги, а тот, кто помогает команде сделать продукт лучше и удобнее для пользователя.\n\n"
        "**О моём обучении:** Я активно учусь и использую современные инструменты, включая искусственный интеллект, чтобы быстрее осваивать новые технологии. Каждый проект я разбираю до деталей — так я расту как специалист."
    )
    await message.answer(
        about_text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=create_main_keyboard()
    )

@dp.message(Command("contacts"))
async def cmd_contacts(message: types.Message):
    contacts_text = (
        "📞 **Мои контакты:**\n\n"
        "• **Email:** Volsar20141991@yandex.com\n"
        "• **GitHub:** [lexi1509](https://github.com/lexi1509)\n"
        "• **Telegram:** @Alexi1509\n"
        "• **Сайт-портфолио:** http://127.0.0.1:5003"
    )
    await message.answer(
        contacts_text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=create_main_keyboard()
    )

@dp.message(Command("site"))
async def cmd_site(message: types.Message):
    site_text = (
        "🌟 **Мой сайт-портфолио**\n\n"
        "Ты можешь посмотреть все мои проекты, навыки и информацию обо мне в удобном формате на сайте:\n"
        "http://127.0.0.1:5003\n\n"
        "Там представлены:\n"
        "• Мои проекты (Telegram Bot и другие)\n"
        "• Контактная информация\n"
        "• Форма обратной связи"
    )
    await message.answer(
        site_text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=create_main_keyboard()
    )

@dp.callback_query(F.data == "about")
async def process_callback_about(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    
    about_text = (
        "ℹ️ **Обо мне:**\n\n"
        "Я начинающий специалист по тестированию, живу и работаю в Саратове. Мой путь в IT начался с изучения Python и желания понять, как создаются и совершенствуются цифровые продукты.\n\n"
        "Для меня тестирование — это не просто рутинная проверка, а увлекательный процесс исследования продукта. Я использую современные инструменты, такие как MySQL для работы с базами данных, Flask для понимания backend-логики и Telegram API для создания pet-проектов. Эти проекты помогают мне не только прокачивать технические навыки, но и видеть полную картину создания продукта — от идеи до реализации.\n\n"
        "Мой подход к работе строится на трёх китах: внимательность к деталям, ответственность за результат и постоянное стремление к развитию. Я убеждена, что хороший тестировщик — это не просто тот, кто находит баги, а тот, кто помогает команде сделать продукт лучше и удобнее для пользователя.\n\n"
        "**О моём обучении:** Я активно учусь и использую современные инструменты, включая искусственный интеллект, чтобы быстрее осваивать новые технологии. Каждый проект я разбираю до деталей — так я расту как специалист."
    )
    
    await bot.send_message(
        callback_query.from_user.id,
        about_text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=create_main_keyboard()
    )

@dp.callback_query(F.data == "contacts")
async def process_callback_contacts(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    
    contacts_text = (
        "📞 **Мои контакты:**\n\n"
        "• **Email:** Volsar20141991@yandex.com\n"
        "• **GitHub:** [lexi1509](https://github.com/lexi1509)\n"
        "• **Telegram:** @Alexi1509\n"
        "• **Сайт-портфолио:** http://127.0.0.1:5003"
    )
    
    await bot.send_message(
        callback_query.from_user.id,
        contacts_text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=create_main_keyboard()
    )

@dp.message()
async def handle_unknown(message: types.Message):
    await message.answer(
        "Я понимаю только команды и кнопки. Используй меню ниже 👇",
        reply_markup=create_main_keyboard()
    )

async def main():
    logger.info("🚀 Бот запущен и слушает события...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())