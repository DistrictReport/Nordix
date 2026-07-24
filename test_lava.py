import asyncio
import json

from payments.lava import lava


async def main():
    invoice = await lava.create_invoice(
        email="123456789@nordix.local",
        amount=100,
    )

    print(json.dumps(invoice, indent=4, ensure_ascii=False))


asyncio.run(main())