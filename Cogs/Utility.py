from discord.ext import commands

class Utility(commands.Cog):
    def __init__(self, APP):
        self.APP = APP
        
    @commands.command(name="Ping")
    async def ping(self, ctx):
        await ctx.send("Pong!")

def setup(APP):
    APP.add_cog(Utility(APP))