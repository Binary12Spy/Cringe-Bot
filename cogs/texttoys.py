import nextcord
from nextcord.ext import commands

import uwuify

slash_categories = {
    ...
}

category_aliases = {
    ...
}

class TextToys(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @nextcord.slash_command(name="uwuify")
    async def uwuify_slash(self, ctx, text: str):
        await ctx.send(uwuify.uwu(text))
        
    @nextcord.message_command(name="uwuify message")
    async def uwuify_message(self, interaction: nextcord.Interaction, message: nextcord.Message):
        response = uwuify.uwu(message.content)
        await message.reply(response)

def setup(bot):
    bot.add_cog(TextToys(bot))