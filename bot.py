import os
import nextcord
from dotenv import load_dotenv
from nextcord.ext import commands

from textwrap import dedent

load_dotenv()
BOT_TOKEN = os.environ.get("BOT_TOKEN")

intents = nextcord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print("Bot logged in")
    
cogignore = file = open("./.cogignore", "r").read().split("\n")

def cog_ignored(cog):
    return cog in cogignore

# Load all non-ignored cogs
for file in os.listdir("./cogs"):
    try:
        if file.endswith(".py"):
            if cog_ignored(file[:-3]):
                continue
            bot.load_extension(f"cogs.{file[:-3]}")
            print(f"Loaded {file[:-3]}!")
    except Exception as e:
        print(f"Failed to load cog {file}: {e}")
        
@bot.command()
async def load(ctx, extension):
    # If the cog is ignored, don't load it unless the user forces it
    if cog_ignored(extension) and not "force" in ctx.message.content:
        await ctx.send(dedent(f"""
                       Cog {extension} is ignored!
                       Send `!load {extension} force` to load it.
                       """))
        return
    
    bot.load_extension(f"cogs.{extension}")
    print(f"Loaded {extension}!")
    await ctx.send(f"Loaded {extension}!")
    
@bot.command()
async def unload(ctx, extension):
    bot.unload_extension(f"cogs.{extension}")
    print(f"Unloaded {extension}!")
    await ctx.send(f"Unloaded {extension}!")
    
@bot.command()
async def reload(ctx, extension):
    # If the cog is ignored, don't reload it unless the user forces it
    if cog_ignored(extension) and not "force" in ctx.message.content:
        await ctx.send(dedent(f"""
                       Cog {extension} is ignored!
                       Send `!reload {extension} force` to reload it.
                       """))
        return
    
    # If the cog isn't loaded, load it
    cog = bot.get_cog(extension)
    if cog is None:
        await load(ctx, extension)
        return
    
    bot.reload_extension(f"cogs.{extension}")
    print(f"Reloaded {extension}!")
    await ctx.send(f"Reloaded {extension}!")

bot.run(BOT_TOKEN)