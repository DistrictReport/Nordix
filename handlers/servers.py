from aiogram import Router
from aiogram.types import Message

from keyboards.menu import main_menu

router = Router()


@router.message(lambda message: message.text == "🌍 Серверы")
async def servers(message: Message):
    await message.answer(
        """
🌍 <b>Серверы Nordix</b>

🇳🇱 Amsterdam (Нидерланды)

🟢 Статус: Онлайн
⚡ Скорость: До 1 Гбит/с
🔒 Протокол: WireGuard

🚀 В ближайшее время появятся новые локации:

🇩🇪 Германия
🇫🇮 Финляндия
🇺🇸 США

Спасибо, что пользуетесь <b>Nordix</b> ❤️
""",
        parse_mode="HTML",
    )
