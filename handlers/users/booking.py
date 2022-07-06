from datetime import timedelta, datetime, time
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.utils.callback_data import CallbackData

from loader import dp, bot
from aiogram.dispatcher.filters import Command, Text
from aiogram import types

from utils.db_api.db_commands import read_free_tables, create_booking_tables, delete_booking

booking_cd=CallbackData("booking","time","level","table","is_upd","is_del")
def make_booking_cd(level, time='0',table='0',is_upd='0',is_del='0'):
    return booking_cd.new(time=time,level=level, table=table, is_upd=is_upd, is_del=is_del)


@dp.message_handler(Command("booking"))
async def welcome_booking(message: types.Message):
    cur_level=0;
    text = f'{message.from_user.full_name}, вы перешли в раздел бронирования стола.\nЕсли вы столкнулись с' \
           f'трудностью при бронировании, нажмите /contacts '
    message.answer(text=text)
    markup = InlineKeyboardMarkup(row_width=3)
    times = []
    now = datetime.now()
    if now.hour<10:
        now = datetime(year=now.year,month=now.month,day=now.day, hour=10,minute=0)
    if now.minute<30:
        now = datetime(year=now.year,month=now.month,day=now.day,hour=now.hour,minute=30)
    else:
        now = datetime(year=now.year,month=now.month,day=now.day,hour=now.hour,minute=0)
        now+=timedelta(hours=1)
    new_datetime = now+timedelta(minutes=30)
    times.append(now.strftime("%H-%M"))
    times.append(new_datetime.strftime("%H-%M"))
    while new_datetime.hour!=0:
        new_datetime+=timedelta(minutes=30)
        times.append(new_datetime.strftime("%H-%M"))
    for item in times:
        markup.insert(
            InlineKeyboardButton(
                text=item,
                callback_data=make_booking_cd(level=cur_level+1, time=item))
        )
    await message.answer(text='Сегодня есть свободные столики на это время:', reply_markup=markup)


async def free_table(callback: CallbackQuery, cur_time, cur_level):
    tables = await read_free_tables(cur_time)
    markup = InlineKeyboardMarkup(row_width=2)
    photo="F:\\pythonProject\\restProject\\img\\"
    iter=0
    for table in tables:
        iter+=1
        photo+=str(table.is_free)
        text=f"Столик №{iter}"
        if table.is_free==0:
            markup.insert(
                InlineKeyboardButton(
                    text=text,
                    callback_data=make_booking_cd(level='2', time=cur_time, table=str(table.id)))
            )
    markup.row(
        InlineKeyboardButton(
            text="⬅Назад",
            callback_data=make_booking_cd(level='0'))
    )
    photo+=".png"
    await bot.send_photo(callback.message.chat.id, types.InputFile(photo))
    await callback.message.edit_text(text='Выберите свободный столик: ', reply_markup=markup)




@dp.callback_query_handler(booking_cd.filter())
async def navigate(call: CallbackQuery, callback_data: dict):
    cur_level = callback_data.get("level")
    cur_time = callback_data.get("time")
    cur_table = callback_data.get("table")
    is_upd = callback_data.get("is_upd")
    is_del = callback_data.get("is_del")
    user_id = str(call.message.chat.id)
    if is_upd=='1':
        await delete_booking(cur_table, cur_time)
        await welcome_booking(call.message)
    elif is_del == '1':
        await delete_booking(cur_table, cur_time)
        await call.message.answer(text="Бронь успешно удалена!\n/my_booking")
    elif cur_level=='0':
        await welcome_booking(call.message)
    elif cur_level=='1':
        await free_table(call,cur_time, cur_level)
    elif cur_level=='2':
        await create_booking_tables(user_id=user_id,table_id=int(cur_table),date=cur_time)
        text=f"Бронирование прошло успешно!\nОтменить бронь вы можете в /profile"
        await call.message.answer(text=text)
