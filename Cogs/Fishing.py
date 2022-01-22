import discord, random, time
from discord.ext import commands
##########################################################
def isRegister(author):
    result = "유저정보"
    return result if result else False
###########################################################



###########################################################
class FISHING(commands.Cog):
    def __init__(self, APP):
        self.APP = APP

    @commands.group(name="낚시")
    async def Fishing(self, ctx):
        return await ctx.send(content="낚시 도움말입니다.")

    @Fishing.command(name="시작")
    async def Fishing_Start(self, ctx):
        USER = isRegister(ctx.author)
        if not USER:
            return await ctx.send("회원가입부터 해주세요.")

        msg = await ctx.send("물고기가 낚싯대를 물기를 기다리는 중...")
        time.sleep(random.randint(0, 9) + random.random())

        fish = "물꼬기"
        

        return await ctx.send("낚시 시작!")

    @Fishing.command(name="회원가입")
    async def Fishing_Register(self, ctx):
        if isRegister(ctx.author):
            return await ctx.send("너는 벌써 회원가입이 되어 있다.")
        
        return await ctx.send("회원가입")

    @Fishing.group(name="물고기")
    async def Fishing_Fish(self, ctx):
        return await ctx.send("물고기 도움말들")
    
    @Fishing_Fish.command(name="추가")
    async def Fishing_Fish_Add(self, ctx, LV, NAME, VALUE):
        return await ctx.send("물고기 추가 명령어.")

def setup(APP):
    APP.add_cog(FISHING(APP))