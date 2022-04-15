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
        embed = discord.Embed(title = "**SERVEUR RETIRE**", color = 0xDC143C)
        embed.set_author(name = guild.name, icon_url = guild.icon_url)
        embed.add_field(name = "Name", value = guild.name, inline=True)
        embed.add_field(name = "Description", value = guild.description, inline=True)
        embed.add_field(name = "Owner", value = guild.owner, inline=False)
        embed.add_field(name = "Number of members", value = guild.member_count, inline = False)
        embed.add_field(name = "Number of guilds", value = len(self.bot.guilds), inline = False)
        await self.bot.get_channel(int(os.getenv("CHANNEL_LOGS"))).send(embed=embed)
        database_handler.remove_channel(guild.id)
        database_handler.remove_all_instructions(guild.id)

    
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        embed = discord.Embed(title = "**NOUVEAU SERVEUR !**", color = 0x00FF00)
        embed.set_author(name = guild.name, icon_url = guild.icon_url)
        embed.add_field(name = "Name", value = guild.name, inline=True)
        embed.add_field(name = "Description", value = guild.description, inline=True)
        embed.add_field(name = "Owner", value = guild.owner, inline=False)
        embed.add_field(name = "Number of members", value = guild.member_count, inline = False)
        embed.add_field(name = "Number of guilds", value = len(self.bot.guilds), inline = False)
        await self.bot.get_channel(int(os.getenv("CHANNEL_LOGS"))).send(embed = embed)