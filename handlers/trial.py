from aiogram import Router, F
from aiogram.types import Message, FSInputFile

from services.trial import activate_trial

router = Router()


@router.message(F.text == "🎁 Бесплатно (1 день)")
async def trial(message: Message):
    result = await activate_trial(
        message.from_user.id
    )

    if not result["success"]:
        await message.answer(result["message"])
        return

    await message.answer(
        "✅ Пробная подписка успешно активирована!\n\n"
        "Срок действия: 1 день."
    )

    # Конфигурационный файл WireGuard
    await message.answer_document(
        FSInputFile(result["config"]),
        caption="📄 Конфигурационный файл WireGuard."
    )

    # QR-код (SVG отправляем как документ)
    await message.answer_document(
        FSInputFile(result["qr"]),
        caption="📷 QR-код для быстрого подключения WireGuard."
    )