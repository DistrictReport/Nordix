import asyncio
from datetime import datetime

from database.devices import (
    get_devices,
    update_device_status,
)
from database.subscriptions import (
    deactivate_subscription,
    get_all_active_subscriptions,
)
from vpn.manager import VPNManager


async def subscription_checker():
    """
    Каждые 5 минут проверяет истекшие подписки.
    Если подписка закончилась — отключает VPN.
    """

    manager = VPNManager()

    while True:
        try:
            subscriptions = await get_all_active_subscriptions()

            now = datetime.now()

            for subscription in subscriptions:

                expires = datetime.fromisoformat(
                    subscription["expires_at"]
                )

                if expires > now:
                    continue

                telegram_id = subscription["telegram_id"]

                devices = await get_devices(
                    telegram_id
                )

                for device in devices:

                    try:
                        manager.disable_client(
                            device["client_id"]
                        )
                    except Exception as e:
                        print(
                            f"[SubscriptionChecker] "
                            f"Не удалось отключить "
                            f"{device['client_name']}: {e}"
                        )

                    await update_device_status(
                        device["client_id"],
                        0
                    )

                await deactivate_subscription(
                    telegram_id
                )

                print(
                    f"[SubscriptionChecker] "
                    f"Подписка пользователя "
                    f"{telegram_id} отключена."
                )

        except Exception as e:
            print(
                f"[SubscriptionChecker] Ошибка: {e}"
            )

        await asyncio.sleep(300)