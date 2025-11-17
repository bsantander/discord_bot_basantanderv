from discord.ext import commands
import os

class MinecraftCog(commands.cogs):
    def __init__(self, bot):
        self.bot = bot
    
    

async def setup(bot):
    await bot.add_cog(MinecraftCog(bot))