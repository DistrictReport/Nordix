import asyncio
import json

from payments.lava import lava


async def main():
    invoice = await lava.create_invoice(
        email="test@test.ru",
        amount=100,
    )

    print(json.dumps(invoice, indent=4, ensure_ascii=False))


asyncio.run(main())