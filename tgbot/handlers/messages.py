from aiogram import types, Router, F
from tgbot.keyboards import workspace_keyboard, database_keyboard

router = Router(name=__name__)


@router.message(F.text == "Изменить рабочую область")
async def workspace_messages_handler(message: types.Message):
    await message.answer(
        "Выберите действие для рабочей области:", reply_markup=workspace_keyboard()
    )


@router.message(F.text == "Изменить базу данных")
async def database_messages_handler(message: types.Message):
    await message.answer(
        "Выберите действие для базы данных:", reply_markup=database_keyboard()
    )
