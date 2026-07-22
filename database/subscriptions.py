from datetime import datetime, timedelta

from database.database import get_db


async def get_subscription(telegram_id: int):
    db = await get_db()

    cursor = await db.execute(
        """
        SELECT *
        FROM subscriptions
        WHERE telegram_id = ?
        """,
        (telegram_id,)
    )

    subscription = await cursor.fetchone()

    await cursor.close()
    await db.close()

    return subscription


async def get_active_subscription(telegram_id: int):
    db = await get_db()

    cursor = await db.execute(
        """
        SELECT *
        FROM subscriptions
        WHERE telegram_id = ?
        AND is_active = 1
        LIMIT 1
        """,
        (telegram_id,)
    )

    subscription = await cursor.fetchone()

    await cursor.close()
    await db.close()

    return subscription


async def get_all_active_subscriptions():
    db = await get_db()

    cursor = await db.execute(
        """
        SELECT *
        FROM subscriptions
        WHERE is_active = 1
        """
    )

    subscriptions = await cursor.fetchall()

    await cursor.close()
    await db.close()

    return subscriptions


async def create_subscription(
    telegram_id: int,
    tariff: str,
    days: int,
    is_trial: bool = False
):
    expires_at = datetime.now() + timedelta(days=days)

    db = await get_db()

    await db.execute(
        """
        INSERT INTO subscriptions(
            telegram_id,
            tariff,
            is_trial,
            expires_at,
            is_active
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            telegram_id,
            tariff,
            int(is_trial),
            expires_at.isoformat(),
            1
        )
    )

    await db.commit()
    await db.close()


async def extend_subscription(
    telegram_id: int,
    days: int
):
    subscription = await get_subscription(telegram_id)

    if subscription is None:
        return

    now = datetime.now()

    expires = datetime.fromisoformat(
        subscription["expires_at"]
    )

    if expires < now:
        expires = now

    expires += timedelta(days=days)

    db = await get_db()

    await db.execute(
        """
        UPDATE subscriptions
        SET
            expires_at = ?,
            is_active = 1
        WHERE telegram_id = ?
        """,
        (
            expires.isoformat(),
            telegram_id
        )
    )

    await db.commit()
    await db.close()


async def activate_subscription(
    telegram_id: int
):
    db = await get_db()

    await db.execute(
        """
        UPDATE subscriptions
        SET is_active = 1
        WHERE telegram_id = ?
        """,
        (telegram_id,)
    )

    await db.commit()
    await db.close()


async def deactivate_subscription(
    telegram_id: int
):
    db = await get_db()

    await db.execute(
        """
        UPDATE subscriptions
        SET is_active = 0
        WHERE telegram_id = ?
        """,
        (telegram_id,)
    )

    await db.commit()
    await db.close()


async def delete_subscription(
    telegram_id: int
):
    db = await get_db()

    await db.execute(
        """
        DELETE FROM subscriptions
        WHERE telegram_id = ?
        """,
        (telegram_id,)
    )

    await db.commit()
    await db.close()


async def subscription_active(
    telegram_id: int
) -> bool:

    subscription = await get_active_subscription(
        telegram_id
    )

    if subscription is None:
        return False

    expires = datetime.fromisoformat(
        subscription["expires_at"]
    )

    if expires <= datetime.now():
        await deactivate_subscription(
            telegram_id
        )
        return False

    return True