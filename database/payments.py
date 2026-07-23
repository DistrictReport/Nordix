from database.database import get_db


async def create_payment(
    telegram_id: int,
    invoice_id: str,
    tariff: str,
    amount: float,
):
    db = await get_db()

    await db.execute(
        """
        INSERT INTO payments(
            telegram_id,
            invoice_id,
            tariff,
            amount,
            status
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            telegram_id,
            invoice_id,
            tariff,
            amount,
            "pending",
        ),
    )

    await db.commit()
    await db.close()


async def get_payment_by_invoice(invoice_id: str):
    db = await get_db()

    cursor = await db.execute(
        """
        SELECT *
        FROM payments
        WHERE invoice_id = ?
        """,
        (invoice_id,),
    )

    payment = await cursor.fetchone()

    await db.close()

    return payment


async def update_payment_status(
    invoice_id: str,
    status: str,
    payment_id: str | None = None,
    provider: str | None = None,
):
    db = await get_db()

    await db.execute(
        """
        UPDATE payments
        SET
            status = ?,
            payment_id = ?,
            provider = ?
        WHERE invoice_id = ?
        """,
        (
            status,
            payment_id,
            provider,
            invoice_id,
        ),
    )

    await db.commit()
    await db.close()


async def payment_exists(invoice_id: str):
    db = await get_db()

    cursor = await db.execute(
        """
        SELECT id
        FROM payments
        WHERE invoice_id = ?
        """,
        (invoice_id,),
    )

    payment = await cursor.fetchone()

    await db.close()

    return payment is not None