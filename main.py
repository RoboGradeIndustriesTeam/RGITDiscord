import discord.ext.commands as commands
from dotenv import load_dotenv
load_dotenv()
import os

bot = commands.Bot(command_prefix="!")

@bot.event
async def on_ready():
    print(f'{bot.user} запущен')

@bot.command()
async def hello(ctx):
    await ctx.send(f"Хай, {ctx.message.author.mention}")

bot.run(os.getenv('TOKEN'))