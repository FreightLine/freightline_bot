from aiogram import Bot, Dispatcher, types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command
import asyncio
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="bot.log",
    filemode="a"
)

# Укажите токен вашего бота
BOT_API_TOKEN = "8103711147:AAFSavuFJwisZOkf2Ax-Wj7g-8_covtMc6M"

# Проверяем, что токен задан
if not BOT_API_TOKEN:
    raise ValueError("Токен бота отсутствует! Пожалуйста, задайте BOT_API_TOKEN.")

# Инициализация бота и диспетчера
bot = Bot(token=BOT_API_TOKEN)
dp = Dispatcher()

# Определяем состояния для регистрации водителя
class DriverRegistration(StatesGroup):
    firm_name = State()
    vehicle_type = State()
    vehicle_number = State()
    vehicle_load = State()
    main_route_pickup = State()
    main_route_dropoff = State()
    return_route_pickup = State()
    return_route_dropoff = State()

# Типы авто
TRUCK_TYPES = [
    "Тентованная (тент / шторка)",
    "Паравоз (тент / шторка)",
    "Изотермическая (изотерм)",
    "Рефрижератор (реф)",
    "Цельнометаллический фургон",
    "Бортовая",
    "Контейнеровоз (20/40 футов)",
    "Автовоз",
    "Самосвал",
    "Цистерна",
    "Трал (низкорамная платформа)",
    "Исузу",
    "Газель"
]

# Клавиатура для выбора типа авто
def get_truck_type_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=2)
    for truck_type in TRUCK_TYPES:
        button = InlineKeyboardButton(text=truck_type, callback_data=f"truck_type_{truck_type.lower()}")
        keyboard.add(button)
    return keyboard

# Команда для запуска регистрации
@dp.message(Command("start_registration"))
async def start_registration(message: types.Message, state: FSMContext):
    await message.answer("Введите название вашей фирмы:")
    await state.set_state(DriverRegistration.firm_name)

# Обработчик: Название фирмы
@dp.message(DriverRegistration.firm_name)
async def process_firm_name(message: types.Message, state: FSMContext):
    await state.update_data(firm_name=message.text)
    await message.answer("Выберите тип авто:", reply_markup=get_truck_type_keyboard())
    await state.set_state(DriverRegistration.vehicle_type)

# Обработчик: Тип авто
@dp.callback_query(DriverRegistration.vehicle_type)
async def process_vehicle_type(callback: CallbackQuery, state: FSMContext):
    if callback.data.startswith("truck_type_"):
        vehicle_type = callback.data.split("_", 2)[2]
        await state.update_data(vehicle_type=vehicle_type)
        await callback.message.edit_text(f"Вы выбрали тип авто: {vehicle_type}.")
        await callback.message.answer("Введите номер авто:")
        await state.set_state(DriverRegistration.vehicle_number)

# Обработчик: Номер авто
@dp.message(DriverRegistration.vehicle_number)
async def process_vehicle_number(message: types.Message, state: FSMContext):
    await state.update_data(vehicle_number=message.text)
    await message.answer("Введите грузоподъемность (в тоннах):")
    await state.set_state(DriverRegistration.vehicle_load)

# Обработчик: Грузоподъемность
@dp.message(DriverRegistration.vehicle_load)
async def process_vehicle_load(message: types.Message, state: FSMContext):
    try:
        load = float(message.text.replace(",", "."))
        await state.update_data(vehicle_load=load)
        await message.answer("Введите место погрузки для основного маршрута:")
        await state.set_state(DriverRegistration.main_route_pickup)
    except ValueError:
        await message.answer("Введите число (например, 20).")

# Обработчик: Основной маршрут - место погрузки
@dp.message(DriverRegistration.main_route_pickup)
async def process_main_route_pickup(message: types.Message, state: FSMContext):
    await state.update_data(main_route_pickup=message.text)
    await message.answer("Введите место выгрузки для основного маршрута:")
    await state.set_state(DriverRegistration.main_route_dropoff)

# Обработчик: Основной маршрут - место выгрузки
@dp.message(DriverRegistration.main_route_dropoff)
async def process_main_route_dropoff(message: types.Message, state: FSMContext):
    await state.update_data(main_route_dropoff=message.text)
    await message.answer("Введите место погрузки для обратного маршрута (если есть):")
    await state.set_state(DriverRegistration.return_route_pickup)

# Обработчик: Обратный маршрут - место погрузки
@dp.message(DriverRegistration.return_route_pickup)
async def process_return_route_pickup(message: types.Message, state: FSMContext):
    await state.update_data(return_route_pickup=message.text)
    await message.answer("Введите место выгрузки для обратного маршрута (если есть):")
    await state.set_state(DriverRegistration.return_route_dropoff)

# Обработчик: Обратный маршрут - место выгрузки
@dp.message(DriverRegistration.return_route_dropoff)
async def process_return_route_dropoff(message: types.Message, state: FSMContext):
    await state.update_data(return_route_dropoff=message.text)
    data = await state.get_data()

    # Финальная информация
    info = (
        f"Регистрация завершена ✅\n\n"
        f"🏢 Фирма: {data.get('firm_name', 'Не указано')}\n"
        f"🚚 Тип авто: {data.get('vehicle_type', 'Не указано')}\n"
        f"🔢 Номер авто: {data.get('vehicle_number', 'Не указано')}\n"
        f"📦 Грузоподъемность: {data.get('vehicle_load', 'Не указано')} т\n"
        f"📍 Основной маршрут: {data.get('main_route_pickup', 'Не указано')} → {data.get('main_route_dropoff', 'Не указано')}\n"
        f"🔄 Обратный маршрут: {data.get('return_route_pickup', 'Не указано')} → {data.get('return_route_dropoff', 'Не указано')}\n"
    )
    await message.answer(info)
