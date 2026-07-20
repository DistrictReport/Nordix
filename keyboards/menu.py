from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🚀 Подключиться")
        ],
        [
            KeyboardButton(text="👤 Профиль"),
            KeyboardButton(text="💎 Подписка")
        ],
        [
            KeyboardButton(text="🌍 Серверы"),
            KeyboardButton(text="🎁 Бесплатно (1 день)")
        ],
        [
            KeyboardButton(text="⚙️ Настройки"),
            KeyboardButton(text="❓ Поддержка")
        ]
    ],
    resize_keyboard=True
)