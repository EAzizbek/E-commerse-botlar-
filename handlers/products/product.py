from aiogram import Router,F
from aiogram.types import Message
from keyboards.inline import inline_products
from states.add_product import AddProductRegister
from aiogram.fsm.context import FSMContext


router=Router()

@router.message(F.text=="Mahsulotlar")
async def product(msg:Message,db):
    products=await db.get_products()
    await msg.answer(text="Mahsulotlar ro'yxati:\n",reply_markup=inline_products(products)
    )

@router.message(F.text=="➕ Mahsulot qo‘shish")
async def add_product(msg:Message,state:FSMContext):
    await msg.answer("Mahsulot qoshish uchun iltimos uning nomini kiriting:")
    await state.set_state(AddProductRegister.name)

@router.message(AddProductRegister.name)
async def add_product(msg:Message,state:FSMContext):
    await state.update_data(name=msg.text)
    await msg.answer("Mahsulot narxini kiriting(so'm da):")
    await state.set_state(AddProductRegister.price)

@router.message(AddProductRegister.price)
async def add_product(msg:Message,state:FSMContext):
    await state.update_data(price=msg.text)
    await msg.answer("Mahsulot tasnifini kiriting: ")
    await state.set_state(AddProductRegister.description)

@router.message(AddProductRegister.description)
async def add_product(msg:Message,state:FSMContext,db):
    await state.update_data(description=msg.text)
    data=await state.get_data()

    await db.add_product(data["name"],data["price"],data["description"])
    await msg.answer("Mahsulot muvaffaqiyatli qoshildi")
    await state.clear()