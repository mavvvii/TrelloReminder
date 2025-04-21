import aiohttp
import asyncio
from datetime import datetime, timezone, timedelta
from config import Settings


class TrelloReminder:
    def __init__(self, settings: Settings) -> None:
        self._settings: Settings = settings
        self._base_url: str = f'https://api.trello.com/1/boards/{settings.trello_board_id}'
        self._session: aiohttp.ClientSession = aiohttp.ClientSession()
        self._members: list[dict[str, str]] = []
        self._cards: list[dict[str, str | list[str]]] = []
        self._alerts: dict[timedelta, str] = {
            timedelta(hours=1): 'You have 1 hour left - dont forget to check off the task!',
            timedelta(days=1): 'You have 1 day left!',
            timedelta(days=3): 'You have 3 days left!',
        }

    async def close(self) -> None:
        await self._session.close()

    async def _fetch(self, path: str, params: dict[str, str]) -> dict:
        url = f'{self._base_url}/{path}'
        query = {'key': self._settings.trello_api_key, 'token': self._settings.trello_api_token}
        if params:
            query.update(params)
        async with self._session.get(url, params=query) as response:
            response.raise_for_status()
            return await response.json()

    async def refresh(self) -> None:
        self._members, self._cards = await asyncio.gather(
            self._fetch('members', {'fields': 'id,fullName'}),
            self._fetch('cards', {'fields': 'id,name,due,idMembers'}),
        )

    def get_cards(self):
        return self._cards

    def get_members(self):
        return self._members

    def compute_due_delta(self, due_str: str) -> timedelta:
        now = datetime.now(timezone.utc)
        due = datetime.fromisoformat(due_str.replace("Z", "+00:00"))
        return due - now

    @property
    def alerts(self) -> dict[timedelta, str]:
        return self._alerts
