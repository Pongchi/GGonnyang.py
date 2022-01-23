import discord
from discord.ext import commands
from RPG.help_command import HELP
from RPG.character import load_Character

class RPG(commands.Cog):
    def __init__(self, APP):
        self.APP = APP
        
    @commands.group(name="캐릭터")
    async def Character(self, ctx):
        if not ctx.invoked_subcommand is None:
            return
        await ctx.message.delete()    
        return await ctx.author.send(embed=HELP("캐릭터"))

    @Character.commands(name="생성")
    async def Character_Create(self, ctx):
        if load_Character(ctx.author.id):
            return await ctx.send("당신은 벌써 캐릭터가 생성되어 있습니다!")
        return await ctx.send("캐릭터 생성을 완료했습니다!")

def setup(APP):
    APP.add_cog(RPG(APP))