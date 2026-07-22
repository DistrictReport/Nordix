from datetime import datetime, timedelta

from aiogram import Router
from aiogram.types import Message

from database.users import get_user
from database.subscriptions import get_active_subscription

router = Router()


@router.message(lambda message: message.text == "👤 Профиль")
async def profile(message: Message):

    user = await get_user(message.from_user.id)

    if user is None:
        await message.answer("❌ Пользователь не найден.")
        return

    subscription = await get_active_subscription(
        message.from_user.id
    )

    telegram_id = user["telegram_id"]
    username = user["username"]
    first_name = user["first_name"]
    trial_activated_at = user["trial_activated_at"]
    created_at = user["created_at"]

    # Пробный период
    if trial_activated_at:
        expires = (
            datetime.fromisoformat(trial_activated_at)
            + timedelta(days=1)
        )

        if expires > datetime.now():
            trial_status = (
                f"✅ До {expires.strftime('%d.%m.%Y %H:%M')}"
            )
        else:
            trial_status = "❌ Истёк"
    else:
        trial_status = "❌ Не использован"

    # Подписка
    if subscription:
        expires = datetime.fromisoformat(
            subscription["expires_at"]
        )

        subscription_text = (
            f"✅ До {expires.strftime('%d.%m.%Y %H:%M')}"
        )
    else:
        subscription_text = "❌ Нет активной подписки"

    username = f"@{username}" if username else "Не указан"

    created = datetime.fromisoformat(
        created_at
    ).strftime("%d.%m.%Y %H:%M")

    await message.answer(
        f"""
👤 <b>Ваш профиль</b>

🆔 ID: <code>{telegram_id}</code>

👤 Имя: {first_name}

📛 Username: {username}

🎁 Пробный период:
{trial_status}

💎 Подписка:
{subscription_text}

📅 Регистрация:
{created}
""",
        parse_mode="HTML"
    )