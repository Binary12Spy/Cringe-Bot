import os
import nextcord
from dotenv import load_dotenv
from nextcord.ext import commands

load_dotenv()
BOT_TOKEN = os.environ.get("BOT_TOKEN")

intents = nextcord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print("Bot logged in")

for file in os.listdir("./cogs"):
    if file.endswith(".py"):
        bot.load_extension(f"cogs.{file[:-3]}")
        
@bot.command
async def load(ctx, extension):
    bot.load_extension(f"cog.{extension}")
    await ctx.send("Loaded cog!")
    
@bot.command
async def unload(ctx, extension):
    bot.unload_extension(f"cog.{extension}")
    await ctx.send("Unloaded cog!")
    
@bot.command
async def reload(ctx, extension):
    bot.reload_extension(f"cog.{extension}")
    await ctx.send("Reloaded cog!")

bot.run(BOT_TOKEN)