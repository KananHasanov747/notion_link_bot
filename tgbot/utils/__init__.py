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
    # BUG: re.VERBOSE string doesn't work here accordingly
    link_pattern = r"""
    \b              # anchors a match to a word boundary
    (               # open parenthesis for grouping
    ?:              # creates a non-capturing group
    http[s]://      # checks whether 'http://' or 'https://' match the description
    |               # designates alternation
    www\.           # otherwise, checks if 'www.' matches the description 
    )               # close parenthesis for grouping
    \S+             # includes the afterwords
    """

    return re.findall(
        link_pattern, text, re.VERBOSE
    )  # re.VERBOSE allows to add 'comments' and 'whitespaces' inside the string


def social_media_extraction(url: str) -> List[str | Any]:
    """Determines popular social media platforms"""
    pass
