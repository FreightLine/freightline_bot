from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Клавиатура для выбора типа фуры
def get_truck_type_keyboard():
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
    keyboard = InlineKeyboardMarkup(row_width=2)
    for truck_type in TRUCK_TYPES:
        keyboard.add(InlineKeyboardButton(text=truck_type, callback_data=f"truck_type_{truck_type.lower()}"))
    return keyboard

# Клавиатура для выбора статуса доступности
def get_availability_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton(text="✅ Да, свободен", callback_data="avail_yes"),
        InlineKeyboardButton(text="❌ Нет, занят", callback_data="avail_no")
    )
    return keyboard