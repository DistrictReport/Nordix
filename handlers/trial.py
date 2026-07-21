from aiogram import Router, F
from aiogram.types import Message, FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder

from services.trial import activate_trial

router = Router()


@router.message(F.text == "🎁 Бесплатно (1 день)")
async def trial(message: Message):
    result = await activate_trial(message.from_user.id)

    if not result["success"]:
        await message.answer(result["message"])
        return

    kb = InlineKeyboardBuilder()

    kb.button(
        text="🍎 Скачать WireGuard (iPhone)",
        url="https://apps.apple.com/app/wireguard/id1441195209",
    )

    kb.button(
        text="🤖 Скачать WireGuard (Android)",
        url="https://play.google.com/store/apps/details?id=com.wireguard.android",
    )

    kb.adjust(1)

    await message.answer(
        "🎉 <b>Ваш VPN готов!</b>\n\n"
        "1️⃣ Установите приложение WireGuard:\n"
        "⬇️ Используйте кнопки ниже.\n\n"
        "2️⃣ Скачайте файл <b>Nordix VPN.conf</b>.\n\n"
        "3️⃣ Откройте WireGuard → ➕ → "
        "<b>Создать из файла или архива</b>.\n\n"
        "4️⃣ Выберите файл и включите VPN.\n\n"
        "🚀 Приятного пользования!",
        parse_mode="HTML",
        reply_markup=kb.as_markup(),
    )

    await message.answer_document(
        FSInputFile(
            result["config"],
            filename="Nordix VPN.conf",
        ),
        caption="📄 Конфигурация WireGuard",
    )