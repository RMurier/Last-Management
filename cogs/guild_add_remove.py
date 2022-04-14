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
        data = database_handler.get_channel(guild.id)
        if data is None:
            return
        chan = guild.get_channel(data["channel_id"])
        try:
            msg = await chan.fetch_message(data["message_id"])
            await msg.delete()
        except Exception as e:
            print(e)
        database_handler.remove_channel(guild.id)
        database_handler.remove_all_instructions(guild.id)