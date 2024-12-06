from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from tgbot.keyboards import start_keyboard

router = Router(name=__name__)


@router.message(CommandStart())
async def start_command_handler(message: types.Message, state: FSMContext):
    from_user = message.from_user

    greeting_text = f"Добро пожаловать, {from_user.full_name}! Чем могу помочь?"

    await message.answer(greeting_text, reply_markup=start_keyboard())
