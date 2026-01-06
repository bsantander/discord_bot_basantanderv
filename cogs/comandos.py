from discord.ext import commands
import os

class ComandosCog(commands.cog):
    def __init__(self, bot):
        self.bot = bot
    
async def setup(bot):
    await bot.add_cog(ComandosCog(bot))