from aiogram.fsm.context import FSMContext
from aiogram import F,Router
from aiogram.types import Message
from states.register import RegisterState

router=Router()

@router.message(F.text=="Register")
async def register(msg:Message,state:FSMContext,db):
    if await db.is_user_exists(msg.from_user.id):
        await msg.answer("Siz allaqachon ro'yxatdan o'tgansz")
    else:
        await msg.answer("Registiratsiyadan o'tish uchun iltimos ismingizni kiriting!")
        await state.set_state(RegisterState.name)

@router.message(RegisterState.name)
async def register(msg:Message,state:FSMContext):
    await state.update_data(name=msg.text)
    await msg.answer("Familyangizni kiriting")
    await state.set_state(RegisterState.surename)

@router.message(RegisterState.surename)
async def register(msg:Message,state:FSMContext):
    await state.update_data(surename=msg.text)
    await msg.answer("Yoshingizni kiriting")
    await state.set_state(RegisterState.age)

@router.message(RegisterState.age)
async def register(msg:Message,state:FSMContext):
    await state.update_data(age=msg.text)
    await msg.answer("Telfon raqamingizni kiriting")
    await state.set_state(RegisterState.phone)

@router.message(RegisterState.phone)
async def register(msg:Message,state:FSMContext,db):
    await state.update_data(phone=msg.text)

    data = await state.get_data()

    await msg.answer(f'Ismingiz: {data['name']}\nFamilyangiz: {data["surename"]}\nYoshingiz: {data['age']}\nTelefon raqamingiz: {data["phone"]}')
    await db.add_user(msg.from_user.id,data["name"],data["surename"],data["age"],data["phone"])
    await state.clear()

