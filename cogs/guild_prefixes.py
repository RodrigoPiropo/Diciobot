import json
import discord
from discord.ext import commands
from discord.utils import get


class Mod_Commands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)

        prefixes[str(guild.id)] = '.'

        with open('prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=4)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)

        prefixes.pop(str(guild.id))

        with open('prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=4)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def changeprefix(self, ctx, prefix):
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)

        prefixes[str(ctx.guild.id)] = prefix

        with open('prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=4)

        await ctx.send(f'Prefix changed to: {prefix}')

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def ping(self, ctx):
        await ctx.send(f'Pong! {round(self.bot.latency, 2)*1000}ms')


def setup(bot):
    bot.add_cog(Mod_Commands(bot))
