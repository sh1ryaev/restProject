from loader import bot
from services.settings_commands import set_default_commands
from utils.db_api.database import create_db
from aiogram import Bot


async def on_startup(dp):
    import filters
    import middlewares
    filters.setup(dp)
    middlewares.setup(dp)

    from utils.notify_admins import on_startup_notify
    await on_startup_notify(dp)
    await create_db()
    await set_default_commands(bot)

if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp

    executor.start_polling(dp, on_startup=on_startup)
