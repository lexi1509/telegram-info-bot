import asyncio
import logging
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.enums import ParseMode

# Загружаем переменные окружения из .env файла
load_dotenv()

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Получаем токен из переменной окружения
BOT_TOKEN = os.getenv('BOT_TOKEN')
if not BOT_TOKEN:
    logger.error("Не задан токен бота! Создайте файл .env с BOT_TOKEN=ваш_токен")
    exit(1)

# Инициализируем бота и диспетчер
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# ============== ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ==============

def create_main_keyboard() -> InlineKeyboardMarkup:
    """Создает клавиатуру с основными кнопками меню."""
    builder = InlineKeyboardBuilder()
    # Кнопки с callback_data (для обработки нажатий)
    builder.row(
        InlineKeyboardButton(text="ℹ️ О проектах", callback_data="about"),
        InlineKeyboardButton(text="📞 Контакты", callback_data="contacts")
    )
    builder.row(
        InlineKeyboardButton(text="📂 Мой GitHub", url="https://github.com/lexi1509")
    )
    builder.row(
        InlineKeyboardButton(text="🛍️ Проект магазина", url="https://github.com/lexi1509/shop_project")
    )
    return builder.as_markup()

# ============== ОБРАБОТЧИКИ КОМАНД ==============

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    """Обработчик команды /start с отправкой фото"""
    user_name = message.from_user.first_name
    logger.info(f"Пользователь {user_name} (id: {message.from_user.id}) запустил бота")
    
    # Текст приветствия
    welcome_text = (
        f"👋 Привет, {user_name}!\n\n"
        "Меня зовут Любовь. Я начинающий специалист по тестированию.\n"
        "С моими проектами можно познакомиться ниже 👇"
    )
    
    # Отправка фото (если файл существует)
    try:
        # Пытаемся отправить фото из файла avatar.jpg
        photo = FSInputFile("avatar.jpg")
        await message.answer_photo(
            photo=photo,
            caption=welcome_text,
            reply_markup=create_main_keyboard()
        )
    except FileNotFoundError:
        # Если фото не найдено, отправляем только текст
        logger.warning("Файл avatar.jpg не найден, отправляю только текст")
        await message.answer(
            welcome_text,
            reply_markup=create_main_keyboard()
        )

@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    """Обработчик команды /help"""
    help_text = (
        "📋 **Доступные команды:**\n\n"
        "/start - Начать работу с ботом\n"
        "/help - Показать эту справку\n"
        "/info - Информация обо мне\n"
        "/contacts - Мои контакты\n\n"
        "Также можно использовать кнопки меню для навигации."
    )
    await message.answer(help_text, parse_mode=ParseMode.MARKDOWN)

@dp.message(Command("info"))
async def cmd_info(message: types.Message):
    """Обработчик команды /info"""
    info_text = (
        "ℹ️ **Обо мне:**\n\n"
        "Меня зовут Любовь Алексеева. Я начинающий специалист по тестированию.\n\n"
        "Мои проекты:\n"
        "• 🛍️ Магазин на Python + MySQL\n"
        "• 🤖 Этот Telegram бот\n\n"
        "Исходный код всех проектов доступен на GitHub."
    )
    await message.answer(
        info_text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=create_main_keyboard()
    )

@dp.message(Command("contacts"))
async def cmd_contacts(message: types.Message):
    """Обработчик команды /contacts"""
    contacts_text = (
        "📞 **Контакты:**\n\n"
        "• **Email:** Volsar20141991@yandex.com\n"
        "• **GitHub:** [lexi1509](https://github.com/lexi1509)\n\n"
        "По всем вопросам обращайтесь!"
    )
    await message.answer(
        contacts_text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=create_main_keyboard()
    )

# ============== ОБРАБОТЧИКИ НАЖАТИЙ НА КНОПКИ (CALLBACK) ==============

@dp.callback_query(F.data == "about")
async def process_callback_about(callback_query: types.CallbackQuery):
    """Обработчик нажатия на кнопку 'О проектах'"""
    await bot.answer_callback_query(callback_query.id)
    
    about_text = (
        "ℹ️ **О моих проектах:**\n\n"
        "• **Shop Project** — консольное и веб-приложение для управления товарами.\n"
        "  Использует Python, MySQL, Flask, SQLTools.\n"
        "• **Telegram Info Bot** — бот-визитка с кнопками на aiogram.\n\n"
        "Код открыт и доступен на GitHub."
    )
    
    await bot.send_message(
        callback_query.from_user.id,
        about_text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=create_main_keyboard()
    )

@dp.callback_query(F.data == "contacts")
async def process_callback_contacts(callback_query: types.CallbackQuery):
    """Обработчик нажатия на кнопку 'Контакты'"""
    await bot.answer_callback_query(callback_query.id)
    
    contacts_text = (
        "📞 **Контакты:**\n\n"
        "• **Email:** Volsar20141991@yandex.com\n"
        "• **GitHub:** [lexi1509](https://github.com/lexi1509)\n\n"
        "По всем вопросам обращайтесь!"
    )
    
    await bot.send_message(
        callback_query.from_user.id,
        contacts_text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=create_main_keyboard()
    )

# ============== ОБРАБОТЧИК ТЕКСТОВЫХ СООБЩЕНИЙ ==============

@dp.message()
async def handle_unknown(message: types.Message):
    """Обработчик любых текстовых сообщений (не команд)"""
    await message.answer(
        "Я понимаю только команды и кнопки. Используй меню ниже 👇",
        reply_markup=create_main_keyboard()
    )

# ============== ЗАПУСК БОТА ==============

async def main():
    """Главная функция запуска бота"""
    logger.info("🚀 Бот запущен и слушает события...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())