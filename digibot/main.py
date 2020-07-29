import logging
import sys
from datetime import datetime

import discord
from discord.ext import commands

from digiformatter import styles, logger as digilogger

from digibot import conf
from digibot.lib import status
from digibot.lib.discordlogger import DiscordHandler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("digibot")
logger.handlers = []
logger.propagate = False
dfhandler = digilogger.DigiFormatterHandler()
logger.addHandler(dfhandler)

initial_cogs = [
    "admin",
    "fun",
    # "help",
    "quote"
]


def main():
    try:
        conf.load()
    except FileNotFoundError as e:
        logger.error(f"Configuration file not found: {e.filename}")
        return

    booting = True
    launchtime = datetime.now()

    bot = commands.Bot(command_prefix = conf.prefix, description = conf.description)

    # bot.remove_command("help")

    for cog in initial_cogs:
        bot.load_extension("digibot.cogs." + cog)

    async def on_first_ready():
        # Set up logging.
        logChannel = bot.get_channel(conf.logchannelid)
        discordhandler = DiscordHandler(logChannel)
        logger.addHandler(discordhandler)

        # Print the splash screen.
        LOGIN = digilogger.addLogLevel("login", fg="cyan")
        logger.log(LOGIN, f"Logged in as: {bot.user.name} ({bot.user.id})\n------")

        # Add a special message to bot status if we are running in debug mode
        activity = discord.Game(name = "DigiBot")
        if conf.activity:
            activity = discord.Game(name = conf.activity)
        if sys.gettrace() is not None:
            activity = discord.Activity(type=discord.ActivityType.listening, name = "DEBUGGER 🔧")

        # More splash screen.
        await bot.change_presence(activity = activity)
        print(styles)
        logger.info(f"Prefix: {conf.prefix}")
        launchfinishtime = datetime.now()
        elapsed = launchfinishtime - launchtime
        logger.debug(f"DigiBot launched in {round((elapsed.total_seconds() * 1000), 3)} milliseconds.\n")
        status.ready()

    async def on_reconnect_ready():
        logger.error("DigiBot has been reconnected to Discord.")

    @bot.event
    async def on_ready():
        # Split on_ready into two events: one when we first boot, and one for reconnects.
        nonlocal booting
        if booting:
            await on_first_ready()
            booting = False
        else:
            await on_reconnect_ready()

    @bot.event
    async def on_message(message):
        await bot.process_commands(message)

    @bot.event
    async def on_message_edit(before, after):
        if before.content == after.content:
            return
        await bot.process_commands(after)

    @bot.event
    async def on_disconnect():
        logger.error("DigiBot has been disconnected from Discord!")

    if not conf.authtoken:
        logger.error(f"Authentication token not found!")
        return

    bot.run(conf.authtoken)


if __name__ == "__main__":
    main()
