import json
import sqlite3
import discord
from discord.ext import commands
from discord.utils import get

def get_prefix(bot, message):
    if message.guild is None:
        return '.'
    else:
        conn = sqlite3.connect('prefixes.db')
        c = conn.cursor()
        c.execute("SELECT prefix FROM prefixes WHERE guild_id=?", (message.guild.id,))
        return str(c.fetchone()[0])
        conn.commit()
        conn.close()

class Mod_Commands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        conn = sqlite3.connect('prefixes.db')
        c = conn.cursor()
        c.execute("INSERT INTO prefixes VALUES (?, ?)", (guild.id, '.'))
        conn.commit()
        conn.close()

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        conn = sqlite3.connect('prefixes.db')
        c = conn.cursor()
        c.execute("DELETE FROM prefixes WHERE guild_id=?", (guild.id, ))
        conn.commit()
        conn.close()

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def changeprefix(self, ctx, prefix):
        conn = sqlite3.connect('prefixes.db')
        c = conn.cursor()
        c.execute("UPDATE prefixes SET prefix=? WHERE guild_id=?", (prefix, ctx.guild.id))
        conn.commit()
        conn.close()

        await ctx.send(f'Prefix changed to: {prefix}')

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def ping(self, ctx):
        await ctx.send(f'Pong! {round(self.bot.latency, 2)*1000}ms')


def setup(bot):
    bot.add_cog(Mod_Commands(bot))
