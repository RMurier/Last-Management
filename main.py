import discord
from discord.ext import commands
from discord_slash import SlashCommand
import os
import dotenv

intents = discord.Intents.all()

dotenv.load_dotenv()

bot = commands.Bot(intents=intents, command_prefix="/", case_insensitive=True, max_messages=None, status=discord.Status.online, activity=discord.Game(name="to help you"))
bot.remove_command("help")
slash = SlashCommand(bot, sync_commands = True, sync_on_cog_reload = True, delete_from_unused_guilds = True)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")

dontcharge = []
for filename in os.listdir("./cogs"):
	if filename not in dontcharge and filename.endswith(".py"):
		try:
			bot.load_extension(f"cogs.{filename[:-3]}")
			print(f"Loaded {filename}")
		except Exception as e:
			print(f"Failed to load {filename}:\n{e}")

bot.run(os.getenv("TOKEN"))