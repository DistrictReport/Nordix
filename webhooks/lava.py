import json
import traceback

from aiohttp import web
from aiogram.types import FSInputFile

from services.payment import activate_payment
from bot_instance import bot


async def lava_webhook(request: web.Request):
    print("\n" + "=" * 70)
    print("🔥 LAVA WEBHOOK")

    try:
        body = await request.text()

        print("RAW BODY:")
        print(body)

        try:
            data = json.loads(body)

            print("\nJSON:")
            print(json.dumps(data, indent=4, ensure_ascii=False))

            email = data.get("buyer", {}).get("email")

            if email:
                try:
                    telegram_id = int(email.split("@")[0])

                    print(f"\n✅ TELEGRAM ID = {telegram_id}")

                    event = data.get("eventType")
                    status = data.get("status")

                    if (
                        event == "payment.success"
                        and status == "completed"
                    ):

                        product_title = data.get(
                            "product",
                            {}
                        ).get(
                            "title",
                            ""
                        ).lower()

                        if "30" in product_title:
                            tariff = "buy_1"
                        elif "90" in product_title:
                            tariff = "buy_3"
                        elif "180" in product_title:
                            tariff = "buy_6"
                        elif "365" in product_title:
                            tariff = "buy_12"
                        else:
                            print("❌ Не удалось определить тариф")
                            return web.json_response(
                                {
                                    "status": "error"
                                }
                            )

                        result = await activate_payment(
                            telegram_id,
                            tariff,
                        )

                        print("\n✅ PAYMENT RESULT:")
                        print(result)

                        if result["success"]:
                            await bot.send_document(
                                chat_id=telegram_id,
                                document=FSInputFile(
                                    str(result["config"])
                                )
                            )

                            print("✅ CONFIG отправлен пользователю")
                        else:
                            print("❌ Ошибка активации:")
                            print(result)

                except Exception:
                    traceback.print_exc()
                    print("\n❌ Ошибка обработки оплаты")

            else:
                print("\n❌ EMAIL NOT FOUND")

        except Exception:
            print("\n❌ Получен не JSON")
            print(body)

    except Exception:
        traceback.print_exc()

    print("=" * 70 + "\n")

    return web.json_response(
        {
            "status": "ok"
        }
    )


def create_app():
    app = web.Application()
    app.router.add_post(
        "/lava/webhook",
        lava_webhook,
    )
    return app