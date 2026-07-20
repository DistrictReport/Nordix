from aiogram import Router
from aiogram.types import Message

from database.users import get_user

router = Router()


@router.message(lambda message: message.text == "👤 Профиль")
async def profile(message: Message):

    user = await get_user(message.from_user.id)

    if user is None:
        await message.answer("❌ Пользователь не найден.")
        return

    telegram_id, username, first_name, is_trial, subscription_until, created_at = user

    trial_status = "✅ Активен" if is_trial else "❌ Использован"

    subscription = (
        subscription_until
        if subscription_until
        else "Нет активной подписки"
    )

    username = f"@{username}" if username else "Не указан"

    await message.answer(
        f"""
👤 <b>Ваш профиль</b>

🆔 ID: <code>{telegram_id}</code>

👤 Имя: {first_name}

📛 Username: {username}

🎁 Пробный период: {trial_status}

💎 Подписка:
{subscription}

📅 Регистрация:
{created_at}
""",
        parse_mode="HTML"
    )