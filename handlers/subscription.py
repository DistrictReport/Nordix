from aiogram import Router, F
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from keyboards.subscription import subscription_keyboard
from payments.lava import lava, LavaAPIError

router = Router()


@router.message(F.text == "💎 Купить подписку")
async def subscription_menu(message: Message):
    await message.answer(
        "<b>💎 Выберите тариф</b>",
        parse_mode="HTML",
        reply_markup=subscription_keyboard,
    )


TARIFFS = {
    "buy_1": ("1 месяц", 100),
    "buy_3": ("3 месяца", 270),
    "buy_6": ("6 месяцев", 500),
    "buy_12": ("12 месяцев", 900),
}


@router.callback_query(F.data.in_(TARIFFS.keys()))
async def buy_subscription(callback: CallbackQuery):
    tariff_name, amount = TARIFFS[callback.data]

    try:
        invoice = await lava.create_invoice(
            email="test@test.ru",  # позже заменим на email пользователя
            amount=amount,
        )

        payment_url = invoice["paymentUrl"]

        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="💳 Оплатить",
                        url=payment_url,
                    )
                ]
            ]
        )

        await callback.message.answer(
            f"""
<b>💎 Тариф:</b> {tariff_name}

<b>💰 Стоимость:</b> {amount} ₽

Нажмите кнопку ниже для оплаты.
""",
            parse_mode="HTML",
            reply_markup=keyboard,
        )

    except LavaAPIError as e:
        await callback.message.answer(
            f"❌ Ошибка создания счёта.\n\n<code>{e}</code>",
            parse_mode="HTML",
        )

    except Exception as e:
        await callback.message.answer(
            f"❌ Неизвестная ошибка.\n\n<code>{e}</code>",
            parse_mode="HTML",
        )

    await callback.answer()