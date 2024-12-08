from aiogram import Bot, Router, types
from aiogram.filters import Command, CommandStart
from aiogram.types import BotCommand, BotCommandScopeDefault

from tgbot.keyboards import start_keyboard
from tgbot.utils import user_exists

router = Router(name=__name__)


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="Запустить бота"),
        BotCommand(command="help_1", description="Помощь с подключением"),
        BotCommand(command="help_2", description="Помощь с использованием"),
    ]
    await bot.set_my_commands(commands, BotCommandScopeDefault())


@router.message(CommandStart())
async def start_command_handler(message: types.Message):
    user = await user_exists(message)

    greeting_text = f"Добро пожаловать, {message.from_user.full_name}! Чем могу помочь?"

    await message.answer(greeting_text, reply_markup=await start_keyboard(user))


@router.message(Command("help_1"))
async def help_command_handler(message: types.Message):
    connection_text = """
    Для работы с ботом вам потребуется следующее:
        1. Иметь учетную запись в <a href="https://www.notion.com/">Notion</a>
        2. Иметь рабочую область (<a href="https://developers.notion.com/docs/create-a-notion-integration">Workspace</a>), а также его ключ (токен)
        3. Иметь базу данных (<a href="https://developers.notion.com/docs/working-with-databases#adding-pages-to-a-database">Database</a>), а также его ключ (токен)
    
    После получения необходимой информации, переходите на /help_2
    """
    await message.answer(text=connection_text)


@router.message(Command("help_2"))
async def help_usage_command_handler(message: types.Message):
    usage_text = """
    Использование:
        • У вас изначально появится возможность только добавлять ссылки с последующим изменением текущих данных (т.е. токенов) после выполнения запроса.
        • Разделение ссылок может быть двумя способами: через пробел или сочетания клавиш "Shift+Enter"
        • После ввода ссылок у вас будет возможность выбрать одну из ссылок для отправки.
        • Процесс выбора будет происходить до тех пор, пока вы не добавите все выбранные вами ссылки для отправки.
        • В противном случаи, вы можете отменить процесс во время выбора ссылок нажав на кнопку <b>Отмена</b>
    """

    await message.answer(text=usage_text)
