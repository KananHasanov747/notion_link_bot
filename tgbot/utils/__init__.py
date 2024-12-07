from sqlalchemy import select
from aiogram.types import CallbackQuery, Message

from tgbot.database import session
from tgbot.models import User


async def user_exists(data: Message | CallbackQuery):
    async with session:
        result = await session.execute(
            select(User).where(User.user_id == data.from_user.id)
        )
        return result.scalars().first() or None
