from database.devices import add_device
from database.subscriptions import (
    create_subscription,
    subscription_active,
)
from database.users import get_user
from vpn.manager import VPNManager
from config.tariffs import TARIFFS


async def activate_payment(
    telegram_id: int,
    tariff: str,
):
    user = await get_user(telegram_id)

    if user is None:
        return {
            "success": False,
            "message": "Пользователь не найден."
        }

    if await subscription_active(telegram_id):
        return {
            "success": False,
            "message": "Подписка уже активна."
        }

    manager = VPNManager()

    client_name = f"user_{telegram_id}"

    bundle = manager.create_client_bundle(client_name)

    client = bundle["client"]

    await add_device(
        telegram_id=telegram_id,
        client_id=client["id"],
        client_name=client_name,
        device_name="Основное устройство"
    )

    tariff_data = TARIFFS[tariff]

    await create_subscription(
        telegram_id=telegram_id,
        tariff=tariff,
        days=tariff_data["days"],
        is_trial=False,
    )

    return {
        "success": True,
        "config": bundle["config"],
        "client": client,
    }