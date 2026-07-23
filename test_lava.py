import asyncio

from payments.lava import lava


async def main():
    invoice = await lava.create_invoice(
        email="test@test.ru",
        amount=100,
    )

    print(invoice)


asyncio.run(main())