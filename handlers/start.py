from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.dispatcher.filters import Command

# Обработчик команды /start
async def start_command(message: Message):
    await message.answer(
        "Добро пожаловать в FreightLine бот! 🎉\n\n"
        "Выберите свою роль:\n"
        "🚚 Перевозчик\n"
        "📦 Грузоотправитель\n"
        "⚙️ Администратор\n\n"
        "Введите /help для получения дополнительной информации."
    )

# Регистрация хэндлера
def register_handlers_start(dp: Dispatcher):
    dp.register_message_handler(start_command, Command("start"))