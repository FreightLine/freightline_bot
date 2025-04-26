from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.filters import Command
from utils.states import ShipperRegistration  # Состояния регистрации грузоотправителя
from keyboards.inline import get_truck_type_keyboard  # Клавиатура для выбора типа фуры
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

router = Router()

# Обработчик команды /shipper_menu
@router.message(Command("shipper_menu"))
async def shipper_menu_command(message: types.Message):
    keyboard = InlineKeyboardMarkup(row_width=2).add(
        InlineKeyboardButton(text="➕ Добавить груз", callback_data="add_cargo"),
        InlineKeyboardButton(text="🔍 Найти перевозчиков", callback_data="find_carriers"),
        InlineKeyboardButton(text="📄 Мои грузы", callback_data="view_cargo"),
    )
    await message.answer("Добро пожаловать в меню грузоотправителя! Выберите действие:", reply_markup=keyboard)

# Обработчик добавления груза
@router.callback_query(lambda callback: callback.data == "add_cargo")
async def add_cargo_handler(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Введите описание груза (например, тип, вес, размеры):")
    await state.set_state(ShipperRegistration.cargo_description)

@router.message(ShipperRegistration.cargo_description)
async def process_cargo_description(message: types.Message, state: FSMContext):
    await state.update_data(cargo_description=message.text)
    await message.answer("Выберите тип фуры, которая вам требуется:", reply_markup=get_truck_type_keyboard())
    await state.set_state(ShipperRegistration.truck_type)

@router.callback_query(ShipperRegistration.truck_type)
async def register_truck_type(callback: CallbackQuery, state: FSMContext):
    if callback.data.startswith("truck_type_"):
        truck_type = callback.data.split("_", 2)[2]
        await state.update_data(truck_type=truck_type)
        await callback.message.edit_text(f"Вы выбрали тип фуры: {truck_type}.")
        await callback.message.answer("Введите условия оплаты (например, предоплата, наличные, перевод):")
        await state.set_state(ShipperRegistration.payment_terms)

@router.message(ShipperRegistration.payment_terms)
async def process_payment_terms(message: types.Message, state: FSMContext):
    await state.update_data(payment_terms=message.text)
    await message.answer("Введите маршрут (например, Москва → Казань):")
    await state.set_state(ShipperRegistration.route)

@router.message(ShipperRegistration.route)
async def process_route(message: types.Message, state: FSMContext):
    await state.update_data(route=message.text)
    data = await state.get_data()

    # Формируем финальную информацию о грузе
    cargo_info = (
        f"Груз добавлен ✅\n\n"
        f"📦 Описание груза: {data['cargo_description']}\n"
        f"🚚 Тип фуры: {data['truck_type']}\n"
        f"💳 Условия оплаты: {data['payment_terms']}\n"
        f"🛣️ Маршрут: {data['route']}"
    )
    await message.answer(cargo_info)
    await state.clear()

# Обработчик поиска перевозчиков
@router.callback_query(lambda callback: callback.data == "find_carriers")
async def find_carriers_handler(callback: CallbackQuery):
    await callback.message.answer("Поиск доступных перевозчиков. Функционал в разработке.")
    await callback.answer()

# Обработчик просмотра грузов
@router.callback_query(lambda callback: callback.data == "view_cargo")
async def view_cargo_handler(callback: CallbackQuery):
    await callback.message.answer("Ваши грузы: \n1. Груз 1 (Москва → Казань)\n2. Груз 2 (Казань → Санкт-Петербург).")
    await callback.answer()