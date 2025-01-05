from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.utils.chat_action import ChatActionSender


from tgbot.keyboards import start_keyboard, links_keyboard
from tgbot.states.all_states import WorkspaceStates, DatabaseStates
from tgbot.utils import user_exists
from tgbot.services.title_extractor import fetch_and_extract_title
from tgbot.services.notion_client import NotionService

router = Router(name=__name__)


@router.callback_query(F.data == "home")
async def home_callback_handler(call: types.CallbackQuery):
    user = await user_exists(call)

    await call.message.answer(
        text="Главное меню", reply_markup=await start_keyboard(user)
    )


@router.callback_query(F.data.endswith(("_workspace", "_database")))
async def token_callback_handler(call: types.CallbackQuery, state: FSMContext):
    context = "workspace" if call.data.endswith("_workspace") else "database"

    if context == "workspace":
        await state.set_state(WorkspaceStates.workspace_id)
        await call.message.answer(
            text="Введите новый токен вашего рабочего условия:",
        )
    else:
        await state.set_state(DatabaseStates.database_id)
        await call.message.answer(text="Введите новый токен вашей базы данных:")


@router.callback_query(F.data.startswith("save_link_"))
async def save_link_callback_handler(call: types.CallbackQuery, state: FSMContext):
    user = await user_exists(call)
    link_index = int(call.data.replace("save_link_", ""))

    data = await state.get_data()
    links = data.get("links", [])
    sources = data.get("sources", [])

    if link_index >= len(links):
        await call.answer("Ошибка: неверный индекс ссылки.", show_alert=True)
        return

    # Get and remove the selected link and source
    selected_link = links.pop(link_index)
    selected_source = sources.pop(link_index)

    # Update the state
    await state.update_data(links=links, sources=sources)

    # Save the selected link
    async with ChatActionSender.typing(
        bot=call.message.bot, chat_id=call.message.chat.id
    ):
        try:
            workspace_id = str(user.workspace_id)
            database_id = str(user.database_id)
            title = str(await fetch_and_extract_title(selected_link)) or ""

            notion = NotionService(workspace_id)
            await notion.add_link(
                database_id=database_id,
                url=selected_link,
                title=title,
                category="",
                source=selected_source or "",
            )

            await call.message.answer(f"Ссылка '{selected_link}' успешно добавлена!")
        except Exception as e:
            await call.answer("Ошибка при сохранении ссылки.", show_alert=True)
            raise e

    # Continue the loop or end it if no links are left
    if links:
        await call.message.answer(
            "Выберите другие ссылки для сохранения или нажмите «Отмена»:",
            reply_markup=links_keyboard(links),
        )
    else:
        await state.clear()
        await call.message.answer(
            "Все ссылки обработаны!",
            reply_markup=await start_keyboard(user),
        )
