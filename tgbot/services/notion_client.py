from datetime import datetime
from notion_client import AsyncClient
from tgbot.database import session
from tgbot.models import Link


class NotionService:
    def __init__(self, notion_token: str) -> None:
        self.client = AsyncClient(auth=notion_token)

    async def add_link(
        self,
        database_id: str,
        url: str,
        title: str = "",
        category: str = "",
        source="",
    ):
        properties = {"url": {"url": url}}

        if title:
            properties["title"] = {"title": [{"text": {"content": title}}]}

        if category:
            properties["category"] = {"select": {"name": category}}

        # Creating a new page in the database
        response = await self.client.pages.create(
            parent={"database_id": database_id}, properties=properties
        )

        session.add(
            Link(
                url=url,
                title=title,
                category=category,
                database_id=database_id,
                source=source,
                timestamp=datetime.now(),
            )
        )

        await session.commit()

        return response
