import asyncio

from discord import Intents
from discord.ext import commands

from config import Settings
from discord_notifier import DiscordNotifier
from reminder_service import ReminderService
from trello_client import TrelloClient


async def main():
    base_settings: Settings = Settings()

    intents: Intents = Intents.default()
    intents.message_content = True
    bot: commands.Bot = commands.Bot(command_prefix="!", intents=intents)

    notifier: DiscordNotifier = DiscordNotifier(bot, base_settings)
    await bot.add_cog(notifier)

    trello_client: TrelloClient = TrelloClient(base_settings)
    reminder_services: ReminderService = ReminderService(
        trello_client=trello_client,
        discord_notifier=notifier,
        interval=base_settings.check_interval,
    )

    task_bot: asyncio.Task = asyncio.create_task(
        bot.start(base_settings.discord_api_token)
    )
    await notifier.ready_event.wait()
    task_reminder = asyncio.create_task(reminder_services.start())
    await asyncio.gather(task_bot, task_reminder)
    await trello_client.close()


if __name__ == "__main__":

    asyncio.run(main())
