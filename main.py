import asyncio

from services.trello_reminder import TrelloReminder
from services.discord_bot import DiscordBot
from services.reminder_coordinator import ReminderCoordinator


async def main():
    trello_reminder: TrelloReminder = TrelloReminder()
    discord_bot: DiscordBot = DiscordBot(trello_reminder)
    reminder_coordinator: ReminderCoordinator = ReminderCoordinator(trello_reminder, discord_bot)

    await reminder_coordinator.run()


if __name__ == "__main__":
    #ToDo using Protocol create better typing structure in directory Protocol
    #ToDo get discord id members using api ?
    #Todo compere discord id to trello id to ping this person that belongs to @Jack You have 1 day left!

    asyncio.run(main())