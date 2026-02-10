from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from keyboards.reply import start_reply

router=Router()

@router.message(CommandStart())
async def start_handler(msg:Message):
    await msg.answer(f"Assalomu Alaykum {msg.from_user.full_name},Botga xush kelibsz",reply_markup=start_reply())