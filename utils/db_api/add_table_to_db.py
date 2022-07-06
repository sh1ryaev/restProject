from utils.db_api.db_commands import create_tables
import asyncio
from utils.db_api.database import create_db


async def create_dishes():
    await create_tables(kolvo_person=4, is_free=0)
    await create_tables(kolvo_person=4, is_free=0)
    await create_tables(kolvo_person=4, is_free=0)
    await create_tables(kolvo_person=4, is_free=0)


loop = asyncio.get_event_loop()
loop.run_until_complete(create_db())
loop.run_until_complete(create_dishes())