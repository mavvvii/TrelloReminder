import asyncio

from discord.ext import commands

from config import Settings
from logger import logger


class DiscordNotifier(commands.Cog):
    def __init__(self, bot: commands.Bot, settings: Settings) -> None:
        super().__init__()
        self.bot = bot
        self.settings = settings
        self.ready_event: asyncio.Event = asyncio.Event()

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        logger.info(f"{self.bot.user} connected to Discord!")
        self.ready_event.set()

    async def send(self, content: str) -> None:
        channel = self.bot.get_channel(int(self.settings.discord_channel_id))
        if not channel:
            logger.warning(
                f"Channel with ID"
                f"{self.settings.discord_channel_id} not found!"
            )
            return
        await channel.send(content)

    # ToDo Add commends for users
    @commands.command(name="tasks")
    async def tasks(self, ctx: commands.Context) -> None:
        await ctx.send("Tasks")
