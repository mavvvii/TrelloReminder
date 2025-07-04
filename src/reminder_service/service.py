import asyncio
from dataclasses import dataclass
from datetime import timedelta
from typing import Set

from discord_notifier import DiscordNotifier
from logger import logger
from trello_client import TrelloClient


@dataclass(frozen=True)
class AlertKey:
    card_id: str
    threshold_date: timedelta

    def __hash__(self) -> int:
        return hash((self.card_id, self.threshold_date))


class ReminderService:
    def __init__(
        self,
        trello_client: TrelloClient,
        discord_notifier: DiscordNotifier,
        interval: int,
    ) -> None:
        self.trello_client = trello_client
        self.discord_notifier = discord_notifier
        self.interval = interval
        self._triggered_alerts: Set[AlertKey] = set()

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
            await self._process_card(card)

    async def _process_card(self, card: dict[str, str | list[str]]) -> None:
        due_date: str = card.get('due')
        if not due_date:
            return

        due_time_left: timedelta = (
            self.trello_client.compute_due_delta(due_date)
        )

        await self._check_alert_threshold(card, due_time_left, due_date)

    async def _check_alert_threshold(
        self,
        card: dict[str, str | list[str]],
        due_time_left: timedelta,
        due_date: str,
    ) -> None:
        alerts = self.trello_client.alerts.items()
        for threshold_date, msg in alerts:
            if self._should_send_alert(
                due_time_left, threshold_date, card['id']
            ):
                await self._send_alert(card, msg, due_date, threshold_date)

    def _should_send_alert(
        self,
        due_time_left: timedelta,
        threshold_date: timedelta,
        card_id: str,
    ) -> bool:
        if not (timedelta(0) <= due_time_left <= threshold_date):
            return False

        alert_key = AlertKey(card_id=card_id, threshold_date=threshold_date)
        return alert_key not in self._triggered_alerts

    async def _send_alert(
        self,
        card: dict,
        alert_msg: str,
        due_date: str,
        alert_threshold: timedelta,
    ) -> None:
        members: list[str] = (
            self.trello_client.get_members_data(card['idMembers'])
        )
        members_str: str = ", ".join(members)

        content: str = (
            f"**{card['name']}** - due on {due_date} - "
            f"**{alert_msg}** - {members_str}"
        )

        await self.discord_notifier.send(content)

        alert_key: AlertKey = AlertKey(
            card_id=card['id'], threshold_date=alert_threshold
        )
        self._triggered_alerts.add(alert_key)
