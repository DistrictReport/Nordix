from database.database import get_db


async def add_device(
    telegram_id: int,
    client_id: str,
    client_name: str,
    device_name: str
):
    db = await get_db()

    await db.execute(
        """
        INSERT INTO devices(
            telegram_id,
            client_id,
            client_name,
            device_name
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            telegram_id,
            client_id,
            client_name,
            device_name
        )
    )

    await db.commit()
    await db.close()


async def get_devices(telegram_id: int):
    db = await get_db()

    cursor = await db.execute(
        """
        SELECT *
        FROM devices
        WHERE telegram_id = ?
        ORDER BY created_at
        """,
        (telegram_id,)
    )

    devices = await cursor.fetchall()

    await cursor.close()
    await db.close()

    return devices


async def get_device(client_id: str):
    db = await get_db()

    cursor = await db.execute(
        """
        SELECT *
        FROM devices
        WHERE client_id = ?
        """,
        (client_id,)
    )

    device = await cursor.fetchone()

    await cursor.close()
    await db.close()

    return device


async def update_device_status(
    client_id: str,
    is_active: int
):
    db = await get_db()

    await db.execute(
        """
        UPDATE devices
        SET is_active = ?
        WHERE client_id = ?
        """,
        (
            is_active,
            client_id
        )
    )

    await db.commit()
    await db.close()


async def delete_device(client_id: str):
    db = await get_db()

    await db.execute(
        """
        DELETE FROM devices
        WHERE client_id = ?
        """,
        (client_id,)
    )

    await db.commit()
    await db.close()