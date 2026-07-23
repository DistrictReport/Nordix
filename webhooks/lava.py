from aiohttp import web


async def lava_webhook(request: web.Request):
    data = await request.json()

    print("=" * 50)
    print("LAVA WEBHOOK")
    print(data)
    print("=" * 50)

    return web.json_response({"status": "ok"})


def create_app():
    app = web.Application()
    app.router.add_post("/lava/webhook", lava_webhook)
    return app