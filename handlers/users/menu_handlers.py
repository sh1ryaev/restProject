import asyncio
import datetime
from typing import Union
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text
from aiogram.types import CallbackQuery, Message, InputMediaPhoto, InlineKeyboardMarkup, InlineKeyboardButton, \
    KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from keyboards.inline.menu_keyboards import menu_cd, categories_keyboard, \
    items_keyboard, item_keyboard, basket_keyboard, create_order
from loader import dp, bot
from states.test import DoOrder
from utils.db_api.database import create_db
from utils.db_api.db_commands import read_dish, read_basket, add_dish_in_basket, delete_basket, plus_basket, \
    minus_basket, create_new_order, read_customer, create_sostav_order, read_dishes

payment_order = CallbackData("payment_order","payment")
new_order = CallbackData("new_order", "payment")

def make_payment_order(payment):
    return payment_order.new(payment=payment)

def make_new_order(payment):
    return new_order.new(payment=payment)


@dp.message_handler(Command("menu"))
async def show_menu(message: types.Message):
    await list_categories(message)


async def list_categories(message: Union[CallbackQuery, Message], **kwargs):
    markup = await categories_keyboard()
    if isinstance(message, Message):
        await message.answer("Наше меню", reply_markup=markup)
    elif isinstance(message, CallbackQuery):
        call = message
        await call.message.edit_reply_markup(markup)


async def list_items(callback: CallbackQuery, category, **kwargs):
    markup = await items_keyboard(category)
    items = await read_dishes(category)
    for item in items:
        await show_item(callback, category=category,
        item_id=item.id)
    inline_btn_1 = InlineKeyboardButton('Ассортимент', callback_data='button1')
    inline_kb1 = InlineKeyboardMarkup().add(inline_btn_1)
    await callback.message.answer("Нажмите /menu чтобы вернуться к просмотру ассортимента")


async def show_item(callback: CallbackQuery, category, item_id):
    markup = item_keyboard(category, item_id)
    item = await read_dish(item_id)
    text = f"{item.name} {item.price}₽\n\n{item.description}"
    await bot.send_photo(callback.message.chat.id, photo=item.photo)
    await callback.message.answer(text=text, reply_markup=markup)


async def show_basket(callback: CallbackQuery, category, **kwargs):
    bas_id = callback.message.chat.id
    markup = await basket_keyboard(category, bas_id)
    basket = await read_basket(bas_id)
    text='Ваш заказ:'+'\n'
    sum=0
    if len(basket) < 1:
        text="Заказ пуст..."
    else:
        for item_in_basket in basket:
            item = await read_dish(item_in_basket.id_prod)
            text+=f"{item.category_name[0]}{item.name}\n 🔹Количество: {item_in_basket.kolvo}шт.\n 🔹Цена: {item.price}₽" \
              f"\n〰〰〰〰〰〰〰〰〰〰〰〰〰〰〰\n"
            sum+=item.price*item_in_basket.kolvo
        text+=f"Общая сумма: {sum}₽"
    # Изменяем сообщение, и отправляем новые кнопки с подкатегориями
    await callback.message.edit_text(text=text, reply_markup=markup)


@dp.callback_query_handler(create_order.filter())
async def do_order(call: CallbackQuery, callback_data: dict):
    bas_id = call.message.chat.id
    basket = await read_basket(bas_id)
    sum = 0
    user = await read_customer(str(bas_id))
    if user == None:
        await call.message.answer("Перед оформлением заказа пройдите регистрацию!\n/register")
    else:
        if len(basket) > 0:
            await state1(call)
        else:
            pass


async def state1(call: CallbackQuery):
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton(
            text=f"Наличные",
            callback_data=make_payment_order(payment="Наличные")
        )
    )
    markup.row(
        InlineKeyboardButton(
            text=f"Картой курьеру",
            callback_data=make_payment_order(payment="Картой курьеру"))
    )
    await call.message.edit_text(text="Выберите способ оплаты:", reply_markup=markup)


@dp.callback_query_handler(payment_order.filter())
async def choise(call: CallbackQuery, callback_data: dict):
    payment = callback_data.get("payment")
    text=""
    sum=0
    bas_id = call.message.chat.id
    basket = await read_basket(bas_id)
    user = await read_customer(str(bas_id))
    for product_in_basket in basket:
        item = await read_dish(product_in_basket.id_prod)
        text+=f"Товар: {item.name}\n Количество: {product_in_basket.kolvo}шт.\n Цена: {item.price}₽" \
              f"\n〰〰〰〰〰〰〰〰〰〰〰〰〰〰〰\n"
        sum+=item.price*product_in_basket.kolvo
    text+=f"Общая сумма: {sum}₽ Тип оплаты: {payment}\nАдрес доставки: {user.address}\n" \
          f"Изменить состав заказа /menu\n" \
          f"Изменить персональные данные /profile"
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton(
            text=f"Подтвердить заказ",
            callback_data=make_new_order(payment=payment)
        )
    )
    await call.message.edit_text(text=text, reply_markup=markup)


@dp.callback_query_handler(new_order.filter())
async def create(call: CallbackQuery, callback_data: dict):
    payment = callback_data.get("payment")
    bas_id = call.message.chat.id
    basket = await read_basket(bas_id)
    sum = 0
    user = await read_customer(str(bas_id))
    for product_in_basket in basket:
        item = await read_dish(product_in_basket.id_prod)
        sum += item.price * product_in_basket.kolvo
    order = await create_new_order(id_user=str(bas_id), summa=sum, order_date=datetime.datetime.now(),
                                   payment_type=payment, address=user.address)
    for product_in_basket in basket:
        item = await read_dish(product_in_basket.id_prod)
        await create_sostav_order(id=order.id, id_user=str(bas_id), id_prod=product_in_basket.id_prod,
                                  price=product_in_basket.price, kolvo=product_in_basket.kolvo)
    await delete_basket(id=bas_id)
    await call.message.edit_text(text="Заказ успешно создан!\nВаши заказы можно посмотреть здесь - /my_orders")


@dp.callback_query_handler(menu_cd.filter())
async def navigate(call: CallbackQuery, callback_data: dict):
    current_level = callback_data.get("level")
    category = callback_data.get("category")
    item_id = int(callback_data.get("item_id"))
    buy = int(callback_data.get("buy"))
    clear = int(callback_data.get("clear"))
    delete = int(callback_data.get("delete"))
    add = int(callback_data.get("add"))
    if buy == 1:
        bas_id = call.message.chat.id
        item = await read_dish(item_id)
        res = await add_dish_in_basket(id = bas_id,
                                    id_prod=item_id,
                                    price=item.price,
                                    kolvo=1)

    if clear == 1:
        bas_id = call.message.chat.id
        await delete_basket(id=bas_id)
    if add == 1:
        bas_id = call.message.chat.id
        await plus_basket(id=bas_id, dish_id=item_id)
    if delete == 1:
        bas_id = call.message.chat.id
        await minus_basket(id=bas_id, dish_id=item_id)

    levels = {
        "0": list_categories,  # Отдаем категории
        "1": list_items,  # Отдаем товары
        "2": show_item,  # Предлагаем купить товар
        "3": show_basket  # Отображаем корзину
    }
    current_level_function = levels[current_level]
    await current_level_function(
        call,
        category=category,
        item_id=item_id
    )
