import asyncio

from aiohttp import web
from aiogram import Dispatcher

from database.database import create_database

from handlers.start import router as start_router
from handlers.profile import router as profile_router
from handlers.trial import router as trial_router
from handlers.admin import router as admin_router
from handlers.servers import router as servers_router
from handlers.channel import router as channel_router
from handlers.subscription import router as subscription_router

from services.subscription_checker import subscription_checker
from webhooks.lava import create_app

from bot_instance import bot


dp = Dispatcher()

dp.include_router(admin_router)
dp.include_router(start_router)
dp.include_router(profile_router)
dp.include_router(trial_router)
dp.include_router(servers_router)
dp.include_router(channel_router)
dp.include_router(subscription_router)


async def start_webhook():
    app = create_app()

    runner = web.AppRunner(app)
    await runner.setup()

    site = web.TCPSite(
        runner,
        host="0.0.0.0",
        port=8080
    )

    await site.start()

    print("✅ LAVA Webhook запущен:")
    print("http://0.0.0.0:8080/lava/webhook")


async def main():
    await create_database()

    asyncio.create_task(subscription_checker())

    await start_webhook()

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())