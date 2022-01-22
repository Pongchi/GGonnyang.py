from discord.ext import commands
from discord_slash import cog_ext, SlashContext

class slash(commands.Cog):
    def __init__(self, APP):
        self.APP = APP
        
    @cog_ext.cog_slash(name="fish")
    async def fishing(self, ctx: SlashContext):
        return await ctx.send("GOOD")

def setup(APP):
    APP.add_cog(slash(APP))