import discord, json
from discord.ext import commands

def load_Character(id):
    result = "캐릭터"
    return result

def HELP(cmd):
    embed=discord.Embed(title="[ RPG 도움말 ]", description="- [] 는 없어도 되는 인자. <>는 꼭 필요한 인자. | 는 '이거나' 라는 뜻.", color=0xe82626)
    if cmd == "캐릭터" or "모두":
        embed.add_field(name="```[ 캐릭터 관련 명령어 ]```", inline=False)
        embed.add_field(name="$캐릭터", value="- 캐릭터 명령어에 대한 명령어들을 봅니다.", inline=False)
        embed.add_field(name="$캐릭터 생성", value="- 캐릭터가 없다면 자신의 캐릭터를 생성합니다.", inline=False)
        embed.add_field(name="$캐릭터 정보 [유저ID]", value="- [유저ID]의 캐릭터 정보를 불러옵니다. 기본값은 자신의 ID", inline=False)

    return embed

def getMonster(place):
    if place == "푸른 초원":
        return "슬라임"
    return "몬스터"
################################################################################
class PLAYER:
    def __init__(self, info):
        self.USER = info[-1]
        self.LV = info[6]//30
        self.NAME = info[1]
        self.STR = info[2]
        self.DEF = info[3]
        self.HP = 20 + int((self.STR * 0.5 + self.DEF * int(self.STR * 0.25)) * 2.5)
        self.MAX_HP = self.HP
        self.AP = info[4]
        self.SP = 0
        self.AGI = info[5]
        
        
    def getData(self, data):
        with open(f".\\Cogs\\RPG\\PLAYER\\{self.USER.id}\\{data}.json") as f:
            return json.load(f)




class GAME:
    def __init__(self, p1, p2):
        self.P1 = PLAYER(p1)
        self.P2 = PLAYER(p2)
##########################################################################################


class RPG(commands.Cog):
    def __init__(self, APP):
        self.APP = APP
        
    @commands.group(name="캐릭터")
    async def Character(self, ctx):
        if not ctx.invoked_subcommand is None:
            return
        await ctx.message.delete()    
        return await ctx.author.send(embed=HELP("캐릭터"))

    @Character.command(name="생성")
    async def Character_Create(self, ctx):
        if load_Character(ctx.author.id):
            return await ctx.send("당신은 벌써 캐릭터가 생성되어 있습니다!")
        return await ctx.send("캐릭터 생성을 완료했습니다!")



    @commands.group(name="모험")
    async def Adventure(self, ctx):
        await ctx.message.delete()
        if not ctx.involked_subcommand is None:
            return
        return await ctx.author.send(embed=HELP("모험"))

    @Adventure.command(name="시작")
    async def Adventure_Start(self, ctx):
        await ctx.message.delete()
        user = load_Character(ctx.author.id)
        if not user:
            return await ctx.send("캐릭터부터 생성해주세요! $캐릭터 생성")
        
        ROOM = GAME(user, "")
        
        


    
def setup(APP):
    APP.add_cog(RPG(APP))