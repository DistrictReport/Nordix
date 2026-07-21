from database.database import get_db


async def user_exists(telegram_id: int) -> bool:
    db = await get_db()

    cursor = await db.execute(
        "SELECT 1 FROM users WHERE telegram_id = ?",
        (telegram_id,)
    )

    result = await cursor.fetchone()

    await cursor.close()
    await db.close()

    return result is not None


async def add_user(
    telegram_id: int,
    username: str | None,
    first_name: str | None
):
    db = await get_db()

    await db.execute(
        """
        INSERT INTO users(
            telegram_id,
            username,
            first_name
        )
        VALUES (?, ?, ?)
        """,
        (
            telegram_id,
            username,
            first_name
        )
    )

    await db.commit()
    await db.close()


async def get_user(telegram_id: int):
    db = await get_db()

    cursor = await db.execute(
        """
        SELECT *
        FROM users
        WHERE telegram_id = ?
        """,
        (telegram_id,)
    )

    user = await cursor.fetchone()

    await cursor.close()
    await db.close()

    return user


async def set_trial_activated(
    telegram_id: int,
    activated_at: str
):
    db = await get_db()

    await db.execute(
        """
        UPDATE users
        SET trial_activated_at = ?
        WHERE telegram_id = ?
        """,
        (
            activated_at,
            telegram_id
        )
    )

    await db.commit()
    await db.close()


async def reset_trial(telegram_id: int):
    db = await get_db()

    await db.execute(
        """
        UPDATE users
        SET trial_activated_at = NULL
        WHERE telegram_id = ?
        """,
        (telegram_id,)
    )

    await db.commit()
    await db.close()


async def delete_user(telegram_id: int):
    db = await get_db()

    await db.execute(
        """
        DELETE FROM users
        WHERE telegram_id = ?
        """,
        (telegram_id,)
    )

    await db.commit()
    await db.close()