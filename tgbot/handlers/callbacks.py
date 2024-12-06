# from sqlalchemy import exists
from aiogram import types, Router, F
from tgbot.keyboards import start_keyboard


router = Router(name=__name__)


@router.callback_query(F.data == "home")
async def home_callback_handler(call: types.CallbackQuery):
    await call.message.answer(text="Главное меню", reply_markup=start_keyboard())


@router.callback_query(F.data.endswith("_workspace"))
async def workspace_callback_handler(call: types.CallbackQuery):
    action = call.data.replace("_workspace", "")

    match action:
        case "add":
            pass
        case "change":
            pass
        case "delete":
            pass
        case _:
            pass


@router.callback_query(F.data.endswith("_database"))
async def database_callback_handler(call: types.CallbackQuery):
    action = call.data.replace("_database", "")

    match action:
        case "add":
            pass
        case "change":
            pass
        case "delete":
            pass
        case _:
            pass
