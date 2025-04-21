import asyncio
import os

from discord import Intents, Client, Message
from typing import Final
from dotenv import load_dotenv

from services.trello_client import TrelloReminder

load_dotenv()


class DiscordBot:
    def __init__(self, trello_reminder: TrelloReminder) -> None:
        self.__DISCORD_API_TOKEN: Final[str] = os.getenv('Discord_API_Token')
        self.__DISCORD_CHANNEL_ID: Final[str] = os.getenv('Discord_Channel_ID')

        if not self.discord_api_token:
            raise ValueError('Discord API Token is empty')
        if not self.discord_channel_id:
            raise ValueError('Discord Channel ID is empty')

        self._trello_reminder: TrelloReminder = trello_reminder

        if not self._trello_reminder:
            raise ValueError('Trello reminder is empty')

        self._bot_ready_event: asyncio.Event = asyncio.Event()

        self._intents: Final[Intents] = Intents.default()
        self._intents.message_content = True
        self._client: Final[Client] = Client(intents=self._intents)

    @property
    def discord_api_token(self) -> str:
        return self.__DISCORD_API_TOKEN

    @property
    def discord_channel_id(self) -> str:
        return self.__DISCORD_CHANNEL_ID

    def register_events(self) -> None:
        self._client.event(self.on_ready)
        self._client.event(self.on_message)
        self._client.event(self.sent_channel_message)

    async def run_bot(self) -> None:
        await self._client.start(token=self.discord_api_token, reconnect=True)

    async def on_ready(self) -> None:
        print(f'{self._client.user} has connected to Discord!')
        self._bot_ready_event.set()

    async def on_message(self, message: Message, task = None) -> None | Message:
        #ToDo do commands to show tasks belong to member
        if message.author == self._client.user:
            return
        if message.content.lower() == '!tasks':
            await self._trello_reminder.refresh_data()
            task = await self._trello_reminder.check_tasks_deadline()
            await message.channel.send(
                        f"📌 Zbliża się deadline zadania: **{task['name']}** (termin: {task['due']})"
                    )

    async def sent_channel_message(self, content: str) -> None | Message:
        channel = self._client.get_channel(int(self.discord_channel_id))
        if channel is None:
            return
        await channel.send(content=content)