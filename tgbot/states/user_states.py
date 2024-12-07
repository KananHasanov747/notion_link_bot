from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message

from sqlalchemy import select

from tgbot.database import session
from tgbot.services.notion_client import NotionService
from tgbot.services.title_extractor import fetch_and_extract_title
from tgbot.models import User


router = Router(name=__name__)


class UserState(StatesGroup):
    workspace_id = State()
    database_id = State()
    add_link = State()


@router.message(UserState.workspace_id)
async def process_user_workspace_token(message: Message, state: FSMContext):
    await state.update_data(workspace_id=message.text)
    await state.set_state(UserState.database_id)
    await message.answer("Введите токен для базы данных:")


@router.message(UserState.database_id)
async def process_user_database_token(message: Message, state: FSMContext):
    data = await state.update_data(database_id=message.text)
    await state.clear()

    try:
        async with session:
            session.add(
                User(
                    user_id=message.from_user.id,
                    workspace_id=data["workspace_id"],
                    database_id=data["database_id"],
                )
            )
            await session.commit()

        await state.set_state(UserState.add_link)
        await message.answer(
            "Ваши данные сохранены! Теперь введите ссылку для добавления:"
        )
    except Exception as e:
        await message.answer("Произошла ошибка при сохранении данных.")
        raise e


# Process to add link from the message
@router.message(UserState.add_link)
async def process_add_link(message: Message, state: FSMContext):
    # Retrieve user from the database
    user_id = message.from_user.id
    async with session:
        result = await session.execute(select(User).where(User.user_id == user_id))
        user = result.scalars().first()

    try:
        workspace_id = str(user.workspace_id)
        database_id = str(user.database_id)
        url = str(message.text)
        title = str(await fetch_and_extract_title(message.text)) or ""

        notion = NotionService(workspace_id)
        await notion.add_link(
            database_id=database_id,
            url=url,
            title=title,
            category="",
        )
        await state.clear()

        await message.answer("Ссылка успешно добавлена!")
    except Exception as e:
        await message.answer("Ошибка при добавлении ссылки. Попробуйте снова:")
        raise e
