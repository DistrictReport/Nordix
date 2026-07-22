from aiogram import Router, F
from aiogram.types import Message
from keyboards.subscription import subscription_keyboard

router = Router()


@router.message(F.text == "💎 Купить подписку")
async def subscription_menu(message: Message):
    await message.answer(
        "<b>💎 Выберите тариф</b>",
        parse_mode="HTML",
        reply_markup=subscription_keyboard
    )