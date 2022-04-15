import discord
from discord.ext import commands
from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_option, create_choice, create_permission
import dotenv
from Data.database_handler import DataBaseHandler

database_handler = DataBaseHandler()

def setup(bot):
    bot.add_cog(AddInstruction(bot))

class AddInstruction(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.has_permissions(administrator=True)
    @cog_ext.cog_slash(name = "add_instruction", description="Add an instruction", guild_ids=[778020762313424976, 923226734558584862], options=[
        create_option(name="name", description="The name of the instruction", option_type=3, required=True),
        create_option(name="priority", description="The priority of the instruction (10 = hight, 0 = low)", option_type=4, required=True, choices=[
            create_choice(name="0", value=0),
            create_choice(name="1", value=1),
            create_choice(name="2", value=2),
            create_choice(name="3", value=3),
            create_choice(name="4", value=4),
            create_choice(name="5", value=5),
            create_choice(name="6", value=6),
            create_choice(name="7", value=7),
            create_choice(name="8", value=8),
            create_choice(name="9", value=9),
            create_choice(name="10", value=10)
        ]),
    ])
    async def _add_instruction(self, ctx, name, priority):
        if not database_handler.channel_exist(ctx.guild.id):
            return await ctx.send("You don't have any channel. Please, type /setup to setup your channel.", hidden=True)
        database_handler.add_instruction(ctx.guild.id, name, priority)
        data = database_handler.get_channel(ctx.guild.id)
        chan = ctx.guild.get_channel(data["channel_id"])
        try:
            instructions = database_handler.get_all_instructions(ctx.guild.id)
            mess = await chan.fetch_message(data["message_id"])
            msg = discord.Embed(title="Last Management", description="Your management :", color=0x00ff00)
            for elem in instructions:
                msg.add_field(name=f"`{elem['ID']}` Priority: {elem['priority']}", value=elem["instruction"], inline=False)
            await mess.edit(embed=msg)
            await ctx.send("Done !", hidden=True)
        except Exception as e:
            return await ctx.send(e) 

    # @commands.has_permissions(administrator=True)
    # @cog_ext.cog_slash(name = "reload", description="Reload the bot", guild_ids=[778020762313424976, 923226734558584862])
    # async def _reload(self, ctx):
    #     if not database_handler.channel_exist(ctx.guild.id):
    #         return await ctx.send("You don't have any channel. Please, type /setup to setup your channel.", hidden=True)
    #     data = database_handler.get_channel(ctx.guild.id)
    #     chan = ctx.guild.get_channel(data["channel_id"])
    #     try:
    #         instructions = database_handler.get_all_instructions(ctx.guild.id)
    #         mess = await chan.fetch_message(data["message_id"])
    #         msg = discord.Embed(title="Last Management", description="Your management :", color=0x00ff00)
    #         for elem in instructions:
    #             msg.add_field(name=f"`{elem['ID']}` Priority: {elem['priority']}", value=elem["instruction"], inline=False)
    #         await mess.edit(embed=msg)
    #         await ctx.send("Done !", hidden=True)
    #     except Exception as e:
    #         return await ctx.send(e) 