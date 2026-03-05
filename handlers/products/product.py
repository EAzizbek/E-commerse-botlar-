from aiogram import Router,F
from aiogram.types import Message,CallbackQuery
from keyboards.inline import inline_products,inline_actions
from states.add_product import AddProductRegister
from states.update_product import UpdateProductState
from aiogram.fsm.context import FSMContext
from filters.filter import RoleFilter

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

@router.callback_query(F.data.startswith("product_"),RoleFilter("admin"))
async def product(call: CallbackQuery):
    product_id = int(call.data.split("_")[1])
    await call.message.answer("Mahsulotni tahrirlash yoki o'chirish:",reply_markup=inline_actions(product_id))
    await call.answer()

@router.callback_query(F.data.startswith("delete_product_"),RoleFilter("admin"))
async def delete_product(call:CallbackQuery,db):
    product_id = int(call.data.split("_")[2])
    await db.delete_product(product_id)
    await call.message.answer("Mahsulot muvaffaqiyatli o'chirildi!")
    await call.answer()

@router.callback_query(F.data.startswith("edit_product_"),RoleFilter("admin"))
async def edit_product(call: CallbackQuery,state:CallbackQuery):
    product_id = int(call.data.split("_")[2])
    await state.set_state(UpdateProductState.product_id)
    await state.update_data(product_id=product_id)
    await call.message.answer("Mahsulotni yangilash uchun nomini kiriting: ")
    await state.set_state(UpdateProductState.name)

@router.message(UpdateProductState.name)
async def product(msg:Message,state:FSMContext):
    await state.update_data(name=msg.text)
    await msg.answer("Mahsulot narxinini kiriting: ")
    await state.set_state(UpdateProductState.price)

@router.message(UpdateProductState.price)
async def product(msg:Message,state:FSMContext):
    await state.update_data(price=int(msg.text))
    await msg.answer("Mahsulot tasnifini kiriting: ")
    await state.set_state(UpdateProductState.description)

@router.message(UpdateProductState.description)
async def product(msg:Message,state:FSMContext,db):
    await state.update_data(description=msg.text)
    data=await state.get_data()
    await db.update_product(
        data["name"],
        data["price"],
        data["description"],
        data["product_id"]
        )
    await msg.answer("Mahsulot muvaffaqiyatli o'zgartirildi!")
    await state.clear()


