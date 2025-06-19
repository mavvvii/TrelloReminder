import asyncio
from discord.ext import commands
from discord import Intents
from trello_client import TrelloClient
from discord_notifier import DiscordNotifier
from reminder_service import ReminderService
from config import Settings

async def main():
    base_settings: Settings = Settings()

    intents: Intents = Intents.default()
    intents.message_content = True
    bot: commands.Bot = commands.Bot(command_prefix='!', intents=intents)

    notifier: DiscordNotifier = DiscordNotifier(bot, base_settings)
    await bot.add_cog(notifier)

    trello_client: TrelloClient = TrelloClient(base_settings)
    reminder_services: ReminderService = ReminderService(
        trello_client = trello_client,
        discord_notifier = notifier,
        interval = base_settings.check_interval
    )
    print('asd')
    task_bot = asyncio.create_task(bot.start(base_settings.discord_api_token))
    from logger import logger
    logger.info(type(task_bot))
    await notifier.ready_event.wait()
    task_reminder = asyncio.create_task(reminder_services.start())
    await asyncio.gather(task_bot, task_reminder)
    await trello_client.close()

if __name__ == "__main__":
    #ToDo using Protocol cto reate better typing structure in directory Protocol

    asyncio.run(main())