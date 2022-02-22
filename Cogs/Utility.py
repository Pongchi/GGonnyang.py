from discord.ext import commands

class Utility(commands.Cog):
    def __init__(self, APP):
        self.APP = APP
        
    @commands.command(name="Ping")
    async def ping(self, ctx):
        await ctx.send("Pong!")

    @commands.command(name="채팅청소")
    async def clearChatting(self, ctx, amount):
        amont = amount if amount <= 100 else 100
        if ctx.author.guild_permissions.manage_messages:
            try:
                await ctx.channel.purge(limit=int(amount))
                await ctx.channel.send(f"**{amount}**개의 메시지를 지웠습니다.")
            except ValueError:
                await ctx.send("청소하실 메시지의 **수**를 입력해주세요.")
        else:
            await ctx.send("권한이 없습니다.")

def setup(APP):
    APP.add_cog(Utility(APP))