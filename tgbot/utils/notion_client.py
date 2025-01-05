from datetime import datetime
from notion_client import AsyncClient
from tgbot.database import session
from tgbot.models import Link


class NotionService:
    def __init__(self, workspace_id: str) -> None:
        """Initiliazing the Notion Service by connecting to the workspace"""
        self.client = AsyncClient(auth=workspace_id)

    async def add_link(
        self,
        database_id: str,
        url: str,
        title: str = "",
        category: str = "",
        priority: str = "",
        source="",
    ):
        properties = {"url": {"url": url}}

        if title:
            properties["title"] = {"title": [{"text": {"content": title}}]}

        if category:
            properties["category"] = {"rich_text": [{"text": {"content": category}}]}

        if priority:
            properties["priority"] = {"rich_text": [{"text": {"content": priority}}]}

        # Creating a new page in the database
        await self.client.pages.create(
            parent={"database_id": database_id}, properties=properties
        )

        session.add(
            Link(
                url=url,
                title=title,
                category=category,
                priority=priority,
                database_id=database_id,
                source=source,
                timestamp=datetime.now(),
            )
        )

        await session.commit()
