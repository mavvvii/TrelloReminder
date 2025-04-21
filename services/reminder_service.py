import asyncio
from datetime import timedelta
from typing import Set
from logger import logger
from services.trello_client import TrelloClient
from services.discord_notifier import DiscordNotifier


class ReminderService:
    def __init__(self, trello_client: TrelloClient, discord_notifier: DiscordNotifier, interval: int) -> None:
        self.trello_client = trello_client
        self.discord_notifier = discord_notifier
        self.interval = interval
        self._triggered_alerts: Set[dict[timedelta, str]] = set()
        self._alerted_ids: Set[str] = set()

    async def start(self) -> None:
        while True:
            try:
                await self.trello_client.refresh()
                await self._check_and_alert()
            except Exception:
                logger.exception('Error in reminder loop')
            await asyncio.sleep(self.interval)

    async def _check_and_alert(self) -> None:
        cards = self.trello_client.get_cards()
        for card in cards:
            due = card.get('due')
            if not due:
                continue
            time_left = self.trello_client.compute_due_delta(due)
            for alert_threshold, msg in self.trello_client.alerts.items():
                if time_left <= alert_threshold and time_left > timedelta(0):
                    key = (card['id'], alert_threshold)
                    print(key)
                    if key not in self._triggered_alerts:
                        content = f"📌 {msg}: **{card['name']}** (due: {due})"
                        await self.discord_notifier.send(content)
                        self._triggered_alerts.add(key)