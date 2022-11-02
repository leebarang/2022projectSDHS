import discord
from discord.ext import commands

import os
import environ

intents = discord.Intents.all()
bot=commands.Bot(command_prefix='/',help_command=None,intents=intents)
playlist = []
loop = False

@bot.command() 
async def 정보(ctx):
    await ctx.send('봇 정보 : 구동 체제 - VScode (Python) 버전 : 3.10.8 *기반 : project POPPY (discord.py : 2.0.1')

TOKEN = str(os.environ["BOT_TOKEN"])

bot.run(TOKEN)
