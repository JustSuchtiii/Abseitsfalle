import discord
import os
import logging
import random
from datetime import datetime

from dotenv import load_dotenv
from discord.ext import tasks


# Intents
intents = discord.Intents.default()

intents.members = True
intents.messages = True
intents.message_content = True
intents.reactions = True


# Bot
bot = discord.Bot(
    intents=intents,
    debug_guilds=[1087465763125862490]
)


# Events
@bot.event
async def on_ready():
    print(f"👋 > {bot.user} ist nun Online!\n🤖 > Warte Auf Befehle...")
    status.start()
    print(f"🕛 > Task gestartet: Status")


# Tasks
@tasks.loop(minutes=2)
async def status():
    team_list = ["FCA", "FCU", "BOC", "SVW", "SVD", "BVB", "SGE", "SCF", "HDH", "TSG", "KOE", "RBL", "B04", "M05", "BMG", "FCB", "STU", "VFB",
                 "BSC", "EBS", "F95", "ELV", "SGF", "HSV", "H96", "FCK", "KSC", "KSV", "FCM", "FCN", "OSN", "SCP", "FCH", "S04", "STP", "WIE"]
    team_home = random.choice(team_list)
    team_list.remove(team_home)
    team_away = random.choice(team_list)

    activity_name = f"{team_home} - {team_away}"

    activity = discord.Streaming(
        name=activity_name,
        url="https://www.twitch.tv/justsuchtiii"
    )

    status = discord.Status.online

    await bot.change_presence(
        activity=activity,
        status=status
    )


# Logging
logger = logging.getLogger("discord")
logger.setLevel(logging.DEBUG)

handler = logging.FileHandler(filename="logs/discord.log", encoding="utf-8", mode="w")
handler.setFormatter(logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s"))

logger.addHandler(handler)


# Startup
if __name__ == "__main__":
    for filename in os.listdir("commands"):
        if filename.endswith(".py"):
            bot.load_extension(f"commands.{filename[:-3]}")

    load_dotenv()
    bot.run(os.getenv("TOKEN"), reconnect=True)