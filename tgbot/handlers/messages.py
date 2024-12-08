from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext

from tgbot.keyboards import cancel_keyboard, token_keyboard
from tgbot.states.user_states import UserState
from tgbot.utils import user_exists

router = Router(name=__name__)


@router.message(F.text == "Изменить токены")
async def token_message_handler(message: types.Message):
    await message.answer(
        text="Выберите токен для изменения:", reply_markup=token_keyboard()
    )


@router.message(F.text == "Добавить ссылки")
async def link_message_handler(message: types.Message, state: FSMContext):
    user = await user_exists(message)

    if user:
        await state.set_state(UserState.links)
        await message.answer(
            text="Введите ссылки для добавления или нажмите «Отмена»:",
            reply_markup=cancel_keyboard(),
        )
    else:
        await state.set_state(UserState.workspace_id)
        await message.answer(text="Введите токен для рабочей области:")
