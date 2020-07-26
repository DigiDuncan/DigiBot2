from pathlib import Path

import appdirs
import toml

from digibot.lib import utils


def getDataDir():
    appname = "digibot"
    appauthor = "DigiDuncan"
    datadir = Path(appdirs.user_data_dir(appname, appauthor))
    return datadir


description = "DigiBot."
prefix = "!"
name = "digibot"
activity = "digibot"
authtoken = None
logchannelid = None

# File paths
datadir = getDataDir()
confpath = datadir / "digibot.conf"


def load():
    global prefix, name, activity, authtoken, logchannelid
    configDict = toml.load(confpath)

    # digibot
    if utils.hasPath(configDict, "digibot.prefix"):
        prefix = utils.getPath(configDict, "digibot.prefix")
    if utils.hasPath(configDict, "digibot.name"):
        name = utils.getPath(configDict, "digibot.name")
    if utils.hasPath(configDict, "digibot.activity"):
        name = utils.getPath(configDict, "digibot.activity")

    # Discord
    if utils.hasPath(configDict, "discord.authtoken"):
        authtoken = utils.getPath(configDict, "discord.authtoken")

    logchannelid = utils.getPath(configDict, "discord.logchannelid")
    if logchannelid is not None:
        logchannelid = int(logchannelid)
