import discord
from discord.ext import commands
from discord.ext.commands import *
import dotenv
import os

dotenv.load_dotenv()


def setup(bot):
    bot.add_cog(Erreurs(bot))

class Erreurs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_slash_command_error(self, ctx, error):
        if isinstance(error, commands.BotMissingPermissions):
            erreur = ""
            for err in error.missing_perms:
                erreur += f"``{err}``,"
            erreur = erreur[:-1]
            return await ctx.send(f"The bot need some permissions:\n{erreur}")
        if isinstance(error, commands.MissingPermissions):
            erreur = ""
            for err in error.missing_perms:
                erreur += f"``{err}``,"
            erreur = erreur[:-1]
            return await ctx.send(f"You don't have the permission: \n{erreur}", hidden=True)
        if isinstance(error, commands.CommandOnCooldown):
            return await ctx.send(f"You're in cooldown. Please retry after {round(error.retry_after)}", hidden=True)
        # else:
        #     embed_support = discord.Embed(title = "Erreur", color = 0xDC143C)
        #     id = requests.put(os.getenv("api_endpoint") + "/errors", json = {"error": str(error), "command": str(ctx.cog.get_commands()[0]) or "Unknow", "user_id": ctx.author.id, "guild_id": ctx.guild.id}).json()["ID"]
        #     embed_support.add_field(name = "ID", value = id, inline = True)
        #     embed_support.add_field(name = "Commande", value = ctx.cog.get_commands()[0], inline=True)
        #     embed_support.add_field(name = "Utilisateur", value = f"{ctx.author.mention} ({ctx.author.id})", inline=False)
        #     embed_support.add_field(name = "Serveur", value = f"{ctx.guild.name} ({ctx.guild.id})", inline=True)
        #     embed_support.add_field(name = "Erreur", value=f"```{error}```", inline = False)
        #     embed = discord.Embed(title = "ERROR", color = 0xDC143C)
        #     embed.set_author(name = ctx.author, icon_url=ctx.author.avatar_url)
        #     embed.add_field(name = "_ _", value = langue.errorcontactsupport.format(id))
        #     msg = await self.bot.get_channel(int(os.getenv("support_bug_channel_id"))).send(embed = embed_support)
        #     requests.patch(os.getenv("api_endpoint") + "/errors", json = {"message_id":msg.id, "id":id})
        #     return await ctx.send(embed = embed, hidden=True)