from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from keyboards.reply import start_reply,register_reply,admin_start_reply
from filters.filter import RoleFilter

router=Router()
@router.message(CommandStart(),RoleFilter("admin"))
async def admin_start(msg:Message):
    await msg.answer("Assalomu Alaykum admin xush kelibsz",reply_markup=admin_start_reply())

@router.message(CommandStart())
async def start_handler(msg:Message,db):
    if await db.is_user_exists(msg.from_user.id):
        await msg.answer(f" Assalomu Alaykum siz allaqachon ro'yxatdan o'tgansz",reply_markup=start_reply())
    else:
        await msg.answer(f"Assalomu Alaykum {msg.from_user.full_name},Botga xush kelibsz",reply_markup=register_reply())