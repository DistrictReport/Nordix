from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


subscription_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="🗓 1 месяц • 100 ₽",
                callback_data="buy_1"
            )
        ],
        [
            InlineKeyboardButton(
                text="🗓 3 месяца • 270 ₽",
                callback_data="buy_3"
            )
        ],
        [
            InlineKeyboardButton(
                text="🗓 6 месяцев • 500 ₽",
                callback_data="buy_6"
            )
        ],
        [
            InlineKeyboardButton(
                text="🗓 12 месяцев • 900 ₽",
                callback_data="buy_12"
            )
        ]
    ]
)