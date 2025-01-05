import re
from typing import Any, List
from sqlalchemy import select
from aiogram.types import CallbackQuery, Message

from tgbot.database import session
from tgbot.models import User


async def user_exists(data: Message | CallbackQuery) -> User | None:
    """Returns User if exists in the database; otherwise, returns None"""
    async with session:
        result = await session.execute(
            select(User).where(User.user_id == data.from_user.id)
        )
        return result.scalars().first() or None


def link_extraction(text: str) -> List[str | Any]:
    """Extracting link(s) from the message.text"""

    # try out the pattern in https://regex101.com
    link_pattern = r"""
    \b              # word boundary to start the match
    (?:             # non-capturing group for URL protocols
        http[s]://  # matches 'http://' or 'https://'
        |           # OR
        www\.       # matches 'www.'
    )               # end of non-capturing group
    \S+             # catches one or more non-whitespace characters (URL body)
    """

    return re.findall(
        link_pattern, text, re.VERBOSE
    )  # re.VERBOSE allows to add 'comments' and 'whitespaces' inside the string


def social_media_extraction(url: str) -> List[str | Any]:
    """Determines popular social media platforms"""
    pass
