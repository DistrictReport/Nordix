from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="💎 Купить подписку")
        ],
        [
            KeyboardButton(text="👤 Профиль")
        ],
        [
            KeyboardButton(text="🌍 Серверы"),
            KeyboardButton(text="🎁 Бесплатно (1 день)")
        ],
        [
            KeyboardButton(text="📢 Наш канал")
        ]
    ],
    resize_keyboard=True
)