import discord
from discord.ext import commands
from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_option, create_choice, create_permission
import dotenv
from Data.database_handler import DataBaseHandler

database_handler = DataBaseHandler()

def setup(bot):
    bot.add_cog(Setup(bot))

class Setup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.has_permissions(administrator=True)
    @cog_ext.cog_slash(name = "setup", description="Setup the bot", guild_ids=[778020762313424976, 923226734558584862], options=[
        create_option(name="channel", description="Channel where le manager wrote", option_type=7, required=True)
    ])
    async def _setup(self, ctx, channel):
        msg = discord.Embed(title="Last Management", description="Your management :", color=0x00ff00)
        instructions = database_handler.get_all_instructions(ctx.guild.id)
        if len(instructions) > 0:
            for elem in instructions:
                msg.add_field(name=f"`{elem['ID']}` Priority: {elem['priority']}", value=elem["instruction"], inline=False)
        else:
            msg.add_field(name="_ _", value="No instructions yet", inline=False)
        msg = await channel.send(embed=msg)
        await ctx.send("Done !", hidden=True)
        await msg.pin()
        if database_handler.channel_exist(ctx.guild.id):
            try:
                data = database_handler.get_channel(ctx.guild.id)
                chan = ctx.guild.get_channel(data["channel_id"])
                mess = await chan.fetch_message(data["message_id"])
                await mess.delete()
            except Exception as e:
                print(e)
                await ctx.send(e)
            return database_handler.edit_channel(ctx.guild.id, channel.id, msg.id)
        return database_handler.add_channel(ctx.guild.id, channel.id, msg.id)


    @commands.Cog.listener()
    async def on_message(self, message):
        if message.type == discord.MessageType.pins_add:
            await message.delete()