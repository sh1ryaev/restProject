from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram import types
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from loader import dp, bot
from states.test import Register
from utils.db_api.db_commands import create_customer, read_customer


@dp.message_handler(Command("register"))
async def register(message: types.Message):
    user_id = message.from_user.id
    user = await read_customer(str(user_id))
    if user != None:
        await message.answer('Вы уже зарегистрированы\n/profile')
    else:
        await message.answer('Вы начали регистрацию,\nВведите своё имя')
        await Register.test1.set()


@dp.message_handler(state=Register.test1)
async def state1(message: types.Message, state: FSMContext):
    name = message.text
    await state.update_data(test1=name)
    await message.answer('Введите номер телефона')
    await Register.test2.set()


@dp.message_handler(state=Register.test2)
async def state2(message: types.Message, state: FSMContext):
    phone = message.text
    await state.update_data(test2=phone)
    await message.answer('Введите адрес доставки')
    await Register.test3.set()


@dp.message_handler(state=Register.test3)
async def state3(message: types.Message, state: FSMContext):
    address = message.text
    await state.update_data(test3=address)
    data = await state.get_data()
    name = data.get('test1')
    phone = data.get('test2')
    address = data.get('test3')
    await message.answer(f'Регистрация успешно завершена\n'
                         f'Ваше имя: {name}\n'
                         f'Номер телефона: {phone}\n'
                         f'Адрес доставки: {address}\n'
                         f'Для изменения личной информации - /my_info')
    user_id = message.from_user.id
    await create_customer(user_id=str(user_id), name=name, phone=phone, address=address)
    await state.finish()








