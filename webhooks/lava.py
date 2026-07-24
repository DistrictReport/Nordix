import json
import traceback
from aiohttp import web


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
                except Exception:
                    print("\n❌ Не удалось извлечь Telegram ID")
            else:
                print("\n❌ EMAIL NOT FOUND")

        except Exception:
            print("\nНе JSON")
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
    app.router.add_post("/lava/webhook", lava_webhook)
    return app