from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from sqlalchemy import select

from tgbot.database import session
from tgbot.models import User

router = Router(name=__name__)


class WorkspaceStates(StatesGroup):
    workspace_id = State()  # workspace_id = token


class DatabaseStates(StatesGroup):
    database_id = State()  # database_id = token


@router.message(WorkspaceStates.workspace_id)
async def process_workspace_add_token(message: Message, state: FSMContext):
    user_id = message.from_user.id
    async with session:
        result = await session.execute(select(User).where(User.user_id == user_id))
        user = result.scalars().first()

        try:
            user.workspace_id = message.text
            await session.commit()
            await state.clear()

            await message.answer("Токен рабочей области успешно изменен!")
        except Exception as e:
            await message.answer("Ошибка при изменении токена.")
            raise e


@router.message(DatabaseStates.database_id)
async def process_database_add_token(message: Message, state: FSMContext):
    user_id = message.from_user.id
    async with session:
        result = await session.execute(select(User).where(User.user_id == user_id))
        user = result.scalars().first()

        try:
            user.database_id = message.text
            await session.commit()
            await state.clear()

            await message.answer("Токен базы данных успешно изменен!")
        except Exception as e:
            await message.answer("Ошибка при изменении токена.")
            raise e
