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
    @cog_ext.cog_slash(name = "delete_instruction", description="Delete an instruction", guild_ids=[778020762313424976, 923226734558584862], options=[
        create_option(name="id", description="The ID of the instruction (at the left of the priority)", option_type=4, required=True),
    ])
    async def _add_instruction(self, ctx, id):
        if not database_handler.channel_exist(ctx.guild.id):
            return await ctx.send("You don't have any channel. Please, type /setup to setup your channel.", hidden=True)
        database_handler.remove_instruction(ctx.guild.id, id)
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
            print(e)
            return await ctx.send(e) 