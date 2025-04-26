from aiogram import Router, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from utils.states import AdminPanel

router = Router()

# Клавиатура для админ-панели
def admin_panel_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton(text="📊 Статистика", callback_data="view_statistics"),
        InlineKeyboardButton(text="👥 Пользователи", callback_data="manage_users"),
        InlineKeyboardButton(text="🚚 Фуры и грузы", callback_data="manage_cargo_trucks"),
        InlineKeyboardButton(text="📣 Рассылка", callback_data="mass_mailing")
    )
    return keyboard

# Обработчик команды /admin_panel
@router.message(Command("admin_panel"))
async def admin_panel_command(message: types.Message):
    await message.answer("Добро пожаловать в админ-панель! Выберите действие:", reply_markup=admin_panel_keyboard())

# Обработчик для просмотра статистики
@router.callback_query(lambda callback: callback.data == "view_statistics")
async def view_statistics(callback: CallbackQuery):
    # Здесь можно подключить логику для получения статистики
    stats = (
        "📊 Статистика:\n"
        "- Пользователи: 120\n"
        "- Активные фуры: 35\n"
        "- Активные грузы: 50\n"
        "- Бронирования: 20\n"
    )
    await callback.message.edit_text(stats)
    await callback.answer()

# Обработчик для управления пользователями
@router.callback_query(lambda callback: callback.data == "manage_users")
async def manage_users(callback: CallbackQuery):
    # Здесь можно подключить логику для управления пользователями
    await callback.message.edit_text("Управление пользователями в разработке.")
    await callback.answer()

# Обработчик для управления фурами и грузами
@router.callback_query(lambda callback: callback.data == "manage_cargo_trucks")
async def manage_cargo_trucks(callback: CallbackQuery):
    # Здесь можно подключить логику для управления фурами и грузами
    await callback.message.edit_text("Управление фурами и грузами в разработке.")
    await callback.answer()

# Обработчик для массовой рассылки
@router.callback_query(lambda callback: callback.data == "mass_mailing")
async def mass_mailing(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Введите сообщение для рассылки:")
    await state.set_state(AdminPanel.manage_users)

@router.message(AdminPanel.manage_users)
async def process_mass_mailing(message: types.Message, state: FSMContext):
    # Здесь можно подключить логику для рассылки сообщения
    await message.answer(f"Сообщение отправлено: {message.text}")
    await state.clear()