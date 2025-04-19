import asyncio
from typing import Set

from services.trello_reminder import TrelloReminder
from services.discord_bot import DiscordBot


class ReminderCoordinator:
    def __init__(self, trello_reminder: TrelloReminder, discord_bot: DiscordBot) -> None:
        self._trello_reminder: TrelloReminder = trello_reminder
        self._discord_bot: DiscordBot = discord_bot

        if not self._trello_reminder:
            raise ValueError('Trello reminder is empty')
        if not self._discord_bot:
            raise ValueError('Discord bot is empty')

        self._tasks: list[dict[str, str | list[str]]] = []
        self._already_alerted_ids: Set = set()

    async def periodic_check_loop(self) -> None:
        while True:
            await self._trello_reminder.refresh_data()
            task: dict[str, str | list[str]] | None = await self._trello_reminder.check_tasks_deadline()

            if task is not None and task['id'] not in self._already_alerted_ids:
                self._tasks.append(task)

            for task in self._tasks:
                if task['id'] not in self._already_alerted_ids:
                    await self._discord_bot.sent_channel_message(
                        f"📌 Zbliża się deadline zadania: **{task['name']}** (termin: {task['due']})"
                    )
                    self._already_alerted_ids.add(task['id'])

            await asyncio.sleep(5)

    async def run(self) -> None:
        self._discord_bot.register_events()

        task_run_bot: asyncio.Task = asyncio.create_task(self._discord_bot.run_bot())
        await self._discord_bot._bot_ready_event.wait()
        task_periodic_check: asyncio.Task = asyncio.create_task(self.periodic_check_loop())

        await asyncio.gather(task_run_bot, task_periodic_check)