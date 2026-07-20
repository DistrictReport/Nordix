from config.tariffs import TARIFFS
from database.devices import get_devices
from database.subscriptions import (
    get_active_subscription,
    subscription_active
)


async def can_add_device(telegram_id: int) -> bool:
    """
    Проверяет, может ли пользователь добавить ещё одно устройство.
    """

    if not await subscription_active(telegram_id):
        return False

    subscription = await get_active_subscription(telegram_id)

    if subscription is None:
        return False

    tariff = subscription["tariff"]

    if tariff not in TARIFFS:
        return False

    limit = TARIFFS[tariff]["devices"]

    devices = await get_devices(telegram_id)

    active_devices = [
        device for device in devices
        if device["is_active"]
    ]

    return len(active_devices) < limit


async def get_device_limit(telegram_id: int) -> int:
    """
    Возвращает лимит устройств по тарифу.
    """

    subscription = await get_active_subscription(telegram_id)

    if subscription is None:
        return 0

    tariff = subscription["tariff"]

    return TARIFFS.get(tariff, {}).get("devices", 0)


async def get_available_slots(telegram_id: int) -> int:
    """
    Возвращает количество свободных мест для устройств.
    """

    limit = await get_device_limit(telegram_id)

    devices = await get_devices(telegram_id)

    active_devices = [
        device for device in devices
        if device["is_active"]
    ]

    return max(0, limit - len(active_devices))