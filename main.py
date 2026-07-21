import asyncio
import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from database.database import create_database

from handlers.start import router as start_router
from handlers.profile import router as profile_router
from handlers.trial import router as trial_router
from handlers.admin import router as admin_router
from handlers.servers import router as servers_router
from handlers.channel import router as channel_router

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

dp.include_router(admin_router)
dp.include_router(start_router)
dp.include_router(profile_router)
dp.include_router(trial_router)
dp.include_router(servers_router)
dp.include_router(channel_router)


async def main():
    await create_database()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())