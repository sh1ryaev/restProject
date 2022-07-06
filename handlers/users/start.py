from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(f'Здравствуйте!\nВас приветствует ресторан FoodCourt\n '
                         f'Нажмите /menu, чтобы ознакомиться с меню\nНажмите /help, чтобы увидеть полный список команд')

