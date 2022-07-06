from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScope, BotCommandScopeDefault


async def set_default_commands(bot:Bot):
    return await bot.set_my_commands(
        commands=[
            BotCommand('help', 'Полный список команд'),
            BotCommand('menu', 'Ассортимент'),
            BotCommand('profile', 'Личная информация'),
            BotCommand('booking', 'Бронирование стола'),
            BotCommand('contacts', 'Контакты')
        ],
        scope=BotCommandScopeDefault(),
    )