from aiogram import Router, F
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from keyboards.subscription import subscription_keyboard
from payments.lava import lava, LavaAPIError
from database.payments import create_payment

router = Router()


@router.message(F.text == "💎 Купить подписку")
async def subscription_menu(message: Message):
    await message.answer(
        "<b>💎 Выберите тариф</b>",
        parse_mode="HTML",
        reply_markup=subscription_keyboard,
    )


TARIFFS = {
    "buy_1": {
        "name": "1 месяц",
        "months": 1,
        "price": 100,
    },
    "buy_3": {
        "name": "3 месяца",
        "months": 3,
        "price": 270,
    },
    "buy_6": {
        "name": "6 месяцев",
        "months": 6,
        "price": 500,
    },
    "buy_12": {
        "name": "12 месяцев",
        "months": 12,
        "price": 900,
    },
}


@router.callback_query(F.data.in_(TARIFFS.keys()))
async def buy_subscription(callback: CallbackQuery):
    tariff = TARIFFS[callback.data]

    telegram_id = callback.from_user.id

    try:
        invoice = await lava.create_invoice(
            telegram_id=telegram_id,
            tariff=callback.data,
            email="test@test.ru",
            amount=tariff["price"],
        )

        invoice_id = invoice["id"]
        payment_url = invoice["paymentUrl"]

        await create_payment(
            telegram_id=telegram_id,
            invoice_id=invoice_id,
            tariff=callback.data,
            amount=tariff["price"],
        )

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
<b>💎 Тариф:</b> {tariff["name"]}

<b>💰 Стоимость:</b> {tariff["price"]} ₽

После успешной оплаты подписка активируется автоматически.
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