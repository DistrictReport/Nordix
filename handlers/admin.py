from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from database.devices import get_devices, delete_device
from database.subscriptions import delete_subscription
from database.users import reset_trial
from vpn.manager import VPNManager

router = Router()

ADMIN_ID = 672832814


@router.message(Command("resettrial"))
async def reset_trial_command(message: Message):

    if message.from_user.id != ADMIN_ID:
        return

    args = message.text.split()

    # Если указан Telegram ID
    if len(args) == 2:
        try:
            telegram_id = int(args[1])
        except ValueError:
            await message.answer(
                "❌ Неверный Telegram ID.\n\n"
                "Пример:\n"
                "/resettrial 123456789"
            )
            return
    else:
        # Если ID не указан — сбрасываем себя
        telegram_id = message.from_user.id

    manager = VPNManager()

    devices = await get_devices(telegram_id)

    for device in devices:
        try:
            manager.delete_client(device["client_id"])
        except Exception as e:
            print(f"Ошибка удаления клиента {device['client_id']}: {e}")

        await delete_device(device["client_id"])

    await delete_subscription(telegram_id)
    await reset_trial(telegram_id)

    await message.answer(
        f"✅ Аккаунт пользователя {telegram_id} полностью сброшен.\n\n"
        "Теперь можно снова активировать пробную подписку."
    )