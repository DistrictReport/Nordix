import httpx

from config.config import (
    LAVA_API_KEY,
    LAVA_API_URL,
    LAVA_OFFER_ID,
)


class LavaAPIError(Exception):
    pass


class LavaClient:
    def __init__(self):
        self.base_url = LAVA_API_URL.rstrip("/")
        self.headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            "X-Api-Key": LAVA_API_KEY,
        }

    async def create_invoice(
        self,
        email: str,
        amount: float,
        telegram_id: int | None = None,
        tariff: str | None = None,
    ) -> dict:
        payload = {
            "email": email,
            "offerId": LAVA_OFFER_ID,
            "currency": "RUB",
            "amount": amount,
            "paymentProvider": "PAY2ME",
            "paymentMethod": "SBP",
        }

        async with httpx.AsyncClient(timeout=20) as client:
            response = await client.post(
                f"{self.base_url}/api/v3/invoice",
                headers=self.headers,
                json=payload,
            )

        if response.status_code != 201:
            raise LavaAPIError(
                f"LAVA ERROR {response.status_code}: {response.text}"
            )

        return response.json()

    async def get_invoice(
        self,
        invoice_id: str,
    ) -> dict:
        async with httpx.AsyncClient(timeout=20) as client:
            response = await client.get(
                f"{self.base_url}/api/v2/invoices/{invoice_id}",
                headers=self.headers,
            )

        if response.status_code != 200:
            raise LavaAPIError(
                f"LAVA ERROR {response.status_code}: {response.text}"
            )

        return response.json()


lava = LavaClient()