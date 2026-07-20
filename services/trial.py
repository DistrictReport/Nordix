from datetime import datetime

from config.tariffs import TARIFFS
from database.devices import add_device
from database.subscriptions import (
    create_subscription,
    subscription_active,
)
from database.users import (
    get_user,
    set_trial_activated,
)
from vpn.manager import VPNManager


async def activate_trial(
    telegram_id: int
):
    """
    Полностью активирует пробную подписку.
    """

    user = await get_user(telegram_id)

    if user is None:
        return {
            "success": False,
            "message": "Пользователь не найден."
        }

    if user["trial_activated_at"] is not None:
        return {
            "success": False,
            "message": "Пробный период уже был использован."
        }

    if await subscription_active(telegram_id):
        return {
            "success": False,
            "message": "У вас уже есть активная подписка."
        }

    manager = VPNManager()

    client_name = f"user_{telegram_id}"

    bundle = manager.create_client_bundle(
        client_name
    )

    client = bundle["client"]

    await add_device(
        telegram_id=telegram_id,
        client_id=client["id"],
        client_name=client_name,
        device_name="Основное устройство"
    )

    tariff = TARIFFS["trial"]

    await create_subscription(
        telegram_id=telegram_id,
        tariff="trial",
        days=tariff["days"],
        is_trial=True
    )

    await set_trial_activated(
        telegram_id,
        datetime.now().isoformat()
    )

    return {
        "success": True,
        "config": bundle["config"],
        "qr": bundle["qr"],
        "client": client
    }