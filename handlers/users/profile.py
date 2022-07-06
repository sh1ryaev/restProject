from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from handlers.users.booking import make_booking_cd
from loader import dp
from states.test import MyInfo
from utils.db_api.db_commands import read_customer, change_name, change_phone, change_address, read_sostav_order, \
    read_order, read_dish, read_booking_tables


@dp.message_handler(Command("profile"))
async def my_info(message: types.Message):
    user_id = message.from_user.id
    user = await read_customer(str(user_id))
    if user==None:
        await message.answer("Сначала пройдите регистрацию!\n/register")
    else:
        await message.answer(f'*Ваша личная информация*\n\n'
                         f'Ваше имя: {user.name}\n'
                         f'Номер телефона: {user.phone}\n'
                         f'Адрес доставки: {user.address}\n',parse_mode="Markdown")
        await message.answer(f'Чтобы изменить имя: /change_name\n'
                         f'Чтобы изменить телефон: /change_phone\n'
                         f'Чтобы изменить адрес: /change_address\n'
                         f'Чтобы посмотреть список заказов:\n /my_orders\n'
                         f'Чтобы посмотреть бронирование:\n /my_booking\n')


@dp.message_handler(Command("my_orders"))
async def my_orders(message: types.Message):
    user_id = str(message.from_user.id)
    orders = await read_order(user_id)
    if len(orders) < 1:
        text = "У вас ещё нет заказов!\nОзнакомтесь с ассортиментом:/menu"
    else:
        text = "Ваши заказы:\n\n"
        for order in orders:
            sostav_order = await read_sostav_order(order.id)
            text+=f'Заказ № {order.id} от {order.order_date}\n'
            for item in sostav_order:
                product = await read_dish(item.id_prod)
                text+=f"{item.kolvo}шт. {product.name} - {product.price}руб.\n"
            text+=f"Общая сумма: {order.summa}\n" \
              f"Тип оплаты: {order.payment_type}\n" \
              f"Адресс доставки: {order.address}\n" \
                  f"〰〰〰〰〰〰〰〰〰〰〰〰〰〰〰\n"
    await message.answer(text)




@dp.message_handler(Command("change_name"))
async def change_n(message: types.Message):
    await message.answer('Напишите ваше новое имя')
    await MyInfo.test1.set()


@dp.message_handler(state=MyInfo.test1)
async def state1(message: types.Message, state: FSMContext):
    name = message.text
    await state.update_data(test1=name)
    user_id = str(message.from_user.id)
    await change_name(user_id=user_id, name=name)
    await state.finish()
    await my_info(message)



@dp.message_handler(Command("change_phone"))
async def change_p(message: types.Message):
    await message.answer('Напишите ваш новый телефон')
    await MyInfo.test2.set()

@dp.message_handler(state=MyInfo.test2)
async def state1(message: types.Message, state: FSMContext):
    phone = message.text
    await state.update_data(test2=phone)
    user_id = str(message.from_user.id)
    await change_phone(user_id=user_id, phone=phone)
    await state.finish()
    await my_info(message)


@dp.message_handler(Command("change_address"))
async def change_a(message: types.Message):
    await message.answer('Напишите ваш новый адрес')
    await MyInfo.test3.set()


@dp.message_handler(state=MyInfo.test3)
async def state1(message: types.Message, state: FSMContext):
    address = message.text
    await state.update_data(test3=address)
    user_id = str(message.from_user.id)
    await change_address(user_id=user_id, address=address)
    await state.finish()
    await my_info(message)


@dp.message_handler(Command("my_booking"))
async def my_booking(message: types.Message):
    user_id = str(message.from_user.id)
    booking = await read_booking_tables(user_id)
    if len(booking) < 1:
        text = "У вас нет брони!\nВы можете оформить её здесь:/booking"
        await message.answer(text=text)
    else:
        markup = InlineKeyboardMarkup(row_width=2)
        for b in booking:
            text = f"Поменять {b.date} №{b.table_id}"
            markup.insert(
                InlineKeyboardButton(
                    text=text,
                    callback_data=make_booking_cd(level=0, table=b.table_id, time=b.date, is_upd=1))
            )
            markup.insert(
                InlineKeyboardButton(
                    text="Отменить бронь",
                    callback_data=make_booking_cd(level=0, table=b.table_id, time=b.date, is_del=1))
            )
        await message.answer(text="Ваша бронь:", reply_markup=markup)

