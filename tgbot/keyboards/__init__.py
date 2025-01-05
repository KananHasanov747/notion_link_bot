from typing import List
from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from tgbot.models import User


def cancel_keyboard():
    kb_list = [[KeyboardButton(text="Отмена")]]

    return ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True)


async def start_keyboard(user: User | None):
    kb_list = [
        [KeyboardButton(text="Добавить ссылки")],
    ]

    # checks if user is recorded in database with tokens
    if user:
        kb_list.append(
            [
                KeyboardButton(text="Изменить токены"),
            ]
        )

    return ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Воспользуйтесь меню:",
    )


def token_keyboard():
    kb_list = [
        [
            InlineKeyboardButton(
                text="Рабочая область", callback_data="change_workspace"
            )
        ],
        [InlineKeyboardButton(text="База данных", callback_data="change_database")],
        [InlineKeyboardButton(text="Вернуться", callback_data="home")],
    ]

    return InlineKeyboardMarkup(inline_keyboard=kb_list, resize_keyboard=True)


def links_keyboard(links: List[str]):
    kb_list = [
        [InlineKeyboardButton(text=link, callback_data=f"save_link_{index}")]
        for index, link in enumerate(links)
    ]

    return InlineKeyboardMarkup(inline_keyboard=kb_list, resize_keyboard=True)
