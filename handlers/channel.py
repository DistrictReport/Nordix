from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

router = Router()


@router.message(F.text == "📢 Наш канал")
async def channel(message: Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📢 Перейти в канал",
                    url="https://t.me/+BRQpuie9wABjOGEy"
                )
            ]
        ]
    )

    await message.answer(
        "📢 Официальный канал Nordix\n\n"
        "Подписывайтесь, чтобы быть в курсе всех обновлений.",
        reply_markup=keyboard
    )