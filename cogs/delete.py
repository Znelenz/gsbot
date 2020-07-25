import discord
from discord.ext import commands
from tabulate import tabulate

from models.character import Character
from utils import *


class Delete(commands.Cog):
    """Delete commands."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def delete(self, ctx, fam_name=''):
        """Deletes users's main character from list. **officers can add an optional family name at the
        end to delete a certain user"""

        try:
            author = ctx.message.author
            if not fam_name:
                member = Character.primary_chars(member = author.id).first()
            else:
                member = Character.primary_chars(fam_name__icontains = fam_name, server = ctx.message.guild.id).first()
                roles = [u.name for u in author.roles]
                if ADMIN_USER not in roles:
                    await ctx.send("Only officers may perform this action")
                    return
            member.delete()
            info = [["Success Deleting User"], ["Character", member.char_name], ["Family", member.fam_name]]
            logActivity('Character {} has been deleted'.format(member.char_name), author.name)
            await ctx.send(codify(tabulate(info)))
        except Exception as e:
            print_error(e)
            await ctx.send(codify("Error deleting user"))

    @commands.command(pass_context=True)
    async def delete_all(self, ctx):
        """****Officers only***** Deletes All Characters from the server"""

        try:
            author = ctx.message.author
            roles = [u.name for u in author.roles]
            if ADMIN_USER not in roles:
                await ctx.send("Only officers may perform this action")
                return
            await ctx.send(codify("Are you sure you want to delete all characters?(times out in 10 secs)\n Reply Yes to confirm"))
            msg = await self.bot.wait_for_message(author=ctx.message.author, content="Yes", timeout=10)
            if msg and msg.content == "Yes":
                Character.objects(server = ctx.message.guild.id).delete()
                await ctx.send(codify("Success Clearing All Characters on Server"))
                return
            await ctx.send(codify("Operation Cancelled"))
        except Exception as e:
            print(e)
            await ctx.send(codify("Error deleting all characters"))


def setup(bot):
    bot.add_cog(Delete(bot))
