from aiogram.types import ReplyKeyboardMarkup,KeyboardButton

def start_reply():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Register")]
        ],
        resize_keyboard=True
    )