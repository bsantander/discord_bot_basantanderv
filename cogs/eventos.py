from discord.ext import commands

class EventosCog(commands.cog):
    def __init__(self,bot):
        self.bot = bot


async def setup(bot):
    await bot.add_cog(EventosCog(bot))