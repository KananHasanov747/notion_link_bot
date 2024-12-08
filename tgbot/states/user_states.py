import re
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message


from tgbot.database import session
from tgbot.models import User
from tgbot.keyboards import links_keyboard, start_keyboard
from tgbot.utils import user_exists
from tgbot.services.source_detection import detect_forward_source


router = Router(name=__name__)


class UserState(StatesGroup):
    workspace_id = State()
    database_id = State()
    links = State()
    sources = State()


# Process to add workspace id from the message
@router.message(UserState.workspace_id)
async def process_user_workspace_token(message: Message, state: FSMContext):
    """
    Retrieves the Workspace ID from the message
    """

    await state.update_data(workspace_id=message.text)
    await state.set_state(UserState.database_id)
    await message.answer("Введите токен для базы данных:")


# Process to add database id from the message
@router.message(UserState.database_id)
async def process_user_database_token(message: Message, state: FSMContext):
    """
    Retrieves the Database ID from the message
    Stores the Workspace & Database IDs in the User's model
    """
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

        await state.set_state(UserState.links)
        await message.answer(
            "Ваши данные сохранены! Теперь введите ссылки для добавления:"
        )
    except Exception as e:
        await message.answer("Произошла ошибка при сохранении данных.")
        raise e


# Process to add link from the message
@router.message(UserState.links)
async def process_add_link(message: Message, state: FSMContext):
    """Adds links to Notion from message"""
    user = await user_exists(message)

    if message.text == "Отмена":
        await state.clear()
        await message.answer(
            "Операция отменена.",
            reply_markup=await start_keyboard(user),
        )
        return

    # Extract links from the text or forwarded message
    links = re.findall(r"(https?://[^\s]+)", message.text)
    source = await detect_forward_source(message)

    if not links:
        await message.answer("Не удалось найти ссылки. Попробуйте снова.")
        return

    # Save links and source in the state
    data = await state.get_data()
    saved_links = data.get("links", [])
    saved_sources = data.get("sources", [])
    saved_links.extend(links)
    saved_sources.extend([source] * len(links))  # Save the source for each link
    await state.update_data(links=saved_links, sources=saved_sources)

    await message.answer(
        "Выберите ссылку для сохранения:", reply_markup=links_keyboard(saved_links)
    )
