import discord, json, pymysql
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

def getMonster(place): # {type:"entity"}
    if place == "푸른 초원":
        return "슬라임"
    return "몬스터"

def isGoPlace(userLV, place):
    return True

def getData(who, id):
        with open(f".\\Cogs\\RPG\\{who}\\{id}.json") as f:
            data = json.load(f)
            return (data['skills'], data['item'])

################################################################################
class PLAYER:
    def __init__(self, info):
        self.type=info["type"]
        self.USER = info["info"]
        self.LV = info["exp"]//30
        self.NAME = info["name"]
        self.STR = info["str"]
        self.DEF = info["def"]
        self.HP = 20 + int((self.STR * 0.5 + self.DEF * int(self.STR * 0.25)) * 2.5)
        self.MAX_HP = self.HP
        self.AP = info["ap"]
        self.money = info["money"]
        self.AGI = info["agi"]
        if self.type == "entity":
            self.value = info["value"]
            self.attribute = info["attr"]
            self.img_url = getData("MONSTER", info['id'])
        else:
            self.skills, self.item, self.img_url = getData("PLAYER", info['id'])

    def showStatus(self):
        embed=discord.Embed(color=0xd2e864)
        embed.set_thumbnail(url=f"{self.img_url}")
        embed.add_field(name=f"{self.NAME}", value=f"Lv.{self.LV}", inline=False)
        embed.add_field(name="[ HP ]", value=f"{self.showHP()}", inline=False)
        return embed

    def showHP(self):
        if self.HP <= 0:
            self.HP = 0
        rate = int((self.HP / self.MAX_HP * 100) // 10)
        return f"{rate * ':red_square:'}{(10-rate) * ':white_large_square:'}\n( {self.HP} / {self.MAX_HP} )"

class GAME:
    async def __init__(self, channel, p1, p2):
        self.channel = channel
        self.P1 = PLAYER(p1)
        self.P2 = PLAYER(p2)

        self.msg1 = await channel.send(embed=self.P2.showStatus())
        if self.P2.type != "entity":
            self.msg2 = await channel.send(embed=self.P1.showStatus())

    
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
    async def Adventure_Start(self, ctx, place):
        await ctx.message.delete()
        user = load_Character(ctx.author.id)
        if not user:
            return await ctx.send("캐릭터부터 생성해주세요! $캐릭터 생성")
        elif not isGoPlace(user[0], place):
            return await ctx.send("없는 장소거나 캐릭터의 레벨이 부족합니다!")

        ROOM = GAME(ctx.channel, user, getMonster(place))
        
        


    
def setup(APP):
    APP.add_cog(RPG(APP))