import asyncio
import logging

import betterlogging as bl
import orjson
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from tgbot import handlers, states
from tgbot.data import config
from tgbot.handlers.commands import set_commands
from tgbot.models import Base
from tgbot.database import engine


def setup_logging():
    log_level = logging.INFO
    bl.basic_colorized_config(level=log_level)
    logger = logging.getLogger(__name__)
    logger.info("Starting bot")


def setup_states(dp: Dispatcher) -> None:
    dp.include_router(states.setup())


def setup_handlers(dp: Dispatcher) -> None:
    dp.include_router(handlers.setup())


def setup_middlewares(dp: Dispatcher) -> None:
    pass


async def setup_database():
    """Connects to database if exists; otherwise, creates a new one"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def setup_aiogram(dp: Dispatcher) -> None:
    setup_states(dp)
    setup_handlers(dp)
    setup_middlewares(dp)


async def aiogram_on_startup_polling(dispatcher: Dispatcher, bot: Bot) -> None:
    await setup_database()
    await setup_aiogram(dispatcher)


async def aiogram_on_shutdown_polling(dispatcher: Dispatcher, bot: Bot) -> None:
    await bot.session.close()
    await dispatcher.storage.close()


async def main():
    setup_logging()

    session = AiohttpSession(
        json_loads=orjson.loads,
    )

    bot = Bot(
        token=config.BOT_TOKEN,
        session=session,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    await set_commands(bot)

    storage = MemoryStorage()

    dp = Dispatcher(
        storage=storage,
    )

    dp.startup.register(aiogram_on_startup_polling)
    dp.shutdown.register(aiogram_on_shutdown_polling)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
