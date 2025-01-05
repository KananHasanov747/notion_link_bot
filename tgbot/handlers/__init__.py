from aiogram import Router

from tgbot.handlers.commands import router as commands_router
from tgbot.handlers.callbacks import router as callbacks_router
from tgbot.handlers.messages import router as messages_router


def setup() -> Router:
    router = Router()

    router.include_routers(commands_router, callbacks_router, messages_router)

    return router
