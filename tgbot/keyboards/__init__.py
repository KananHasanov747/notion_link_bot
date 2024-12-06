from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)


def start_keyboard():
    kb_list = [
        [
            KeyboardButton(text="Изменить рабочую область"),
            KeyboardButton(text="Изменить базу данных"),
        ],
        [KeyboardButton(text="Добавить ссылку")],
    ]

    keyboard = ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Воспользуйтесь меню:",
    )

    return keyboard


def workspace_keyboard():
    kb_list = [
        [
            InlineKeyboardButton(text="Добавить", callback_data="add_workspace"),
            InlineKeyboardButton(text="Изменить", callback_data="change_workspace"),
        ],
        [
            InlineKeyboardButton(text="Удалить", callback_data="delete_workspace"),
            InlineKeyboardButton(text="Вернуться", callback_data="home"),
        ],
    ]

    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list, resize_keyboard=True)

    return keyboard


def database_keyboard():
    kb_list = [
        [
            InlineKeyboardButton(text="Добавить", callback_data="add_database"),
            InlineKeyboardButton(text="Изменить", callback_data="change_database"),
        ],
        [
            InlineKeyboardButton(text="Удалить", callback_data="delete_database"),
            InlineKeyboardButton(text="Вернуться", callback_data="home"),
        ],
    ]

    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list, resize_keyboard=True)

    return keyboard
