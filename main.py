import asyncio
from discord.ext import commands
from discord import Intents
from services.trello_client import TrelloClient
from services.discord_notifier import DiscordNotifier
from services.reminder_service import ReminderService
from config import Settings

async def main():
    base_settings = Settings()

    intents = Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix='!', intents=intents)

    notifier = DiscordNotifier(bot, base_settings)
    await bot.add_cog(notifier)

    trello_client = TrelloClient(base_settings)
    reminder_services = ReminderService(
        trello_client = trello_client,
        discord_notifier = notifier,
        interval = base_settings.check_interval
    )

    task_bot = asyncio.create_task(bot.start(base_settings.discord_api_token))
    await notifier.ready_event.wait()
    task_reminder = asyncio.create_task(reminder_services.start())
    await asyncio.gather(task_bot, task_reminder)
    await trello_client.close()

if __name__ == "__main__":
    #ToDo using Protocol create better typing structure in directory Protocol
    #ToDo get discord id members using api ?
    #Todo compere discord id to trello id to ping this person that belongs to @Jack You have 1 day left!

    asyncio.run(main())