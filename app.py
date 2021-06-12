import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from cogs.guild_prefixes import get_prefix

load_dotenv()
DISCORD_TOKEN =  os.getenv("discord_token")

help_command = commands.DefaultHelpCommand(no_category = 'Other')
bot = commands.Bot(command_prefix=get_prefix, description="Dicionário Bot", help_command=help_command)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    await bot.process_commands(message)

@bot.event
async def on_ready():
    for guild in bot.guilds:
        print(f'Running on {guild.name}')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

bot.run(DISCORD_TOKEN)
