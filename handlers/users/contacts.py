from aiogram import types
from aiogram.dispatcher.filters import Command

from loader import dp


@dp.message_handler(Command("contacts"))
async def contacts(message: types.Message):
    await message.answer("Возник вопрос?\nСвяжитесь с нашим администратором по номеру\n"
                         "+79829828928")