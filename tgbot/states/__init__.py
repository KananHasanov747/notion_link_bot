from aiogram import Router

from tgbot.states.all_states import router as all_states_router
from tgbot.states.user_states import router as user_states_router


def setup() -> Router:
    router = Router(name=__name__)

    router.include_routers(user_states_router, all_states_router)
    return router
