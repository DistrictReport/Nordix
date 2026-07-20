from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from database.users import user_exists, add_user
from keyboards.menu import main_menu

router = Router()


@router.message(CommandStart())
async def start(message: Message):

    if not await user_exists(message.from_user.id):
        await add_user(
            telegram_id=message.from_user.id,
            username=message.from_user.username,
            first_name=message.from_user.first_name
        )

        print(f"Новый пользователь: {message.from_user.id}")

    await message.answer(
        "👋 Добро пожаловать в Nordix!\n\n"
        "🔒 Быстрый, безопасный VPN без ограничений.\n\n"
        "🎁 Новым пользователям доступен бесплатный пробный период на 1 день.\n\n"
        "Выберите действие ниже:",
        reply_markup=main_menu
    )