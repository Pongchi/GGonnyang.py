from ast import Or
from base64 import encode
import discord, json, pymysql
from discord.ext import commands
from collections import OrderedDict

con = pymysql.connect(host='localhost', user="root", password="1219", db="GGonnyang", charset="utf8")
cursor = con.cursor(pymysql.cursors.DictCursor)

def load_Character(id):
    SQL = "SELECT * FROM player where id=%s"

    cursor.execute(SQL, (id))
    return cursor.fetchone()

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
            return json.load(f)

def init_User(author):
    SQL = "INSERT INTO player (id) VALUES (%s)"
    cursor.execute(SQL, (author.id))
    con.commit()

    user_data = OrderedDict()
    user_data['nickname'] = author.display_name
    user_data['skills'] = {"기본공격":{"description":"상대방에게 무기를 휘두른다.", "cast-time":5, "damage":{'str':1.0, 'ap':0.0}}}
    user_data['items'] = {'weapon':{'롱소드':{"description":"처음 시작하는 모험가에게 주는 검이다.", "stat":{"str":2}}}, 'item':{}}
    user_data['using'] = '롱소드'
    
    with open(f'.\\Cogs\\RPG\\PLAYER\\{author.id}.json', 'w', encoding='utf-8') as make_file:
        json.dump(user_data, make_file, ensure_ascii=False, indent="\t")
    return 0

################################################################################
class PLAYER:
    def __init__(self, info):
        self.id = info['id']
        self.type=info["type"]
        self.LV = info["exp"]//30
        self.NAME = info["name"]
        self.STR = info["str"]
        self.DEF = info["def"]
        self.HP = 20 + int((self.STR * 0.5 + self.DEF * int(self.STR * 0.25)) * 2.5)
        self.MAX_HP = self.HP
        self.AP = info["ap"]
        self.MONEY = info["money"]
        self.AGI = info["agi"]
        self.DATA = getData("PLAYER" if self.type != "entity" else "MONSTER", self.id)
        if self.type == "entity":
            self.value = info["value"]
            self.attribute = info["attr"]
        else:
            self.USER = info["info"]

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

        init_User(ctx.author)
        
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
        user['info'] = ctx.author
        if not user:
            return await ctx.send("캐릭터부터 생성해주세요! $캐릭터 생성")
        elif not isGoPlace(user[0], place):
            return await ctx.send("없는 장소거나 캐릭터의 레벨이 부족합니다!")

        ROOM = GAME(ctx.channel, user, getMonster(place))
        
        


    
def setup(APP):
    APP.add_cog(RPG(APP))