from aiogram.types import ReplyKeyboardMarkup,KeyboardButton

def register_reply():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Register")]
        ],
        resize_keyboard=True
    )

def start_reply():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Mahsulotlar"),KeyboardButton(text="Mening buyurtmalarim")],
            [KeyboardButton(text="Profile")]
        ],
        resize_keyboard=True
    )

def admin_start_reply():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Mahsulotlar"),KeyboardButton(text="Mening buyurtmalarim")],
            [KeyboardButton(text="Profile"),KeyboardButton(text="Admin panel")]
        ],
        resize_keyboard=True
    )

def admin_panel_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="➕ Mahsulot qo‘shish")],
            [KeyboardButton(text="📋 Mahsulotlar(Admin)")],
            [KeyboardButton(text="👥 Userlar")],
            [KeyboardButton(text="⬅️ Orqaga")]
        ],
        resize_keyboard=True
    )
