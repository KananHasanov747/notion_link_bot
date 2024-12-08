from aiogram import Router, types
from aiogram.filters import CommandStart

from tgbot.keyboards import start_keyboard
from tgbot.utils import user_exists

router = Router(name=__name__)


@router.message(CommandStart())
async def start_command_handler(message: types.Message):
    user = await user_exists(message)

    greeting_text = f"Добро пожаловать, {message.from_user.full_name}! Чем могу помочь?"

    await message.answer(greeting_text, reply_markup=await start_keyboard(user))
