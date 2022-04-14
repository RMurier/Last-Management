import discord
from discord.ext import commands
import requests
import os
import dotenv
from Data.database_handler import DataBaseHandler

database_handler = DataBaseHandler()

dotenv.load_dotenv()


def setup(bot):
    bot.add_cog(BotJoin(bot))

class BotJoin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        database_handler.remove_channel(guild.id)
        database_handler.remove_all_instructions(guild.id)