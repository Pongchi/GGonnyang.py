import discord, json, pymysql, random
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
    if cmd == "캐릭터" or cmd == "모두":
        embed.add_field(name="```[ 캐릭터 관련 명령어 ]```", value="", inline=False)
        embed.add_field(name="$캐릭터", value="- 캐릭터 명령어에 대한 명령어들을 봅니다.", inline=False)
        embed.add_field(name="$캐릭터 생성", value="- 캐릭터가 없다면 자신의 캐릭터를 생성합니다.", inline=False)
        embed.add_field(name="$캐릭터 정보 [유저ID]", value="- [유저ID]의 캐릭터 정보를 불러옵니다. 기본값은 자신의 ID", inline=False)

    return embed

def getMonster(place, value): # {type:"entity"}
    SQL = "SELECT * FROM monster WHERE place = %s and value=%s"
    cursor.execute(SQL, (place, value))
    monster = random.choice(cursor.fetchall())
    monster['type'] = "entity"
    return monster

def isGoPlace(userLV, place):
    SQL = "SELECT * FROM place WHERE name = %s"
    cursor.execute(SQL, (place))
    place = cursor.fetchone()
    return True if place and userLV >= place['reqLV'] else False

def getData(who, id):
        with open(f".\\Cogs\\RPG\\{who}\\{id}.json", "rt", encoding="UTF8") as f:
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

def addPlayerEXP(id, amount):
    SQL = "UPDATE player SET exp = exp + %s WHERE id = %s"
    cursor.execute(SQL, (amount, id))
    return con.commit()
################################################################################
class PLAYER:
    def __init__(self, info):
        self.id = info['id']
        self.type = info["type"]
        self.DATA = getData("PLAYER" if self.type != "entity" else "MONSTER", self.id)
        self.LV = info["exp"]//30
        self.STR = info["str"]
        self.DEF = info["def"]
        self.AP = info["ap"]
        self.MONEY = info["money"]
        self.AGI = info["agi"]
        if self.type == "entity":
            self.NAME = info["name"]
            self.place = info['place']
            self.value = info["value"]
            self.attribute = info["attr"]
            self.HP = info['hp']
        else:
            self.HP = 20 + int((self.STR * 0.25 + self.DEF * 0.1) * 1.5)
            self.USER = info["info"]
            self.NAME = self.DATA['nickname']
        self.MAX_HP = self.HP

    def showStatus(self):
        embed=discord.Embed(color=0xd2e864)
        if self.type == "entity":
            embed.set_thumbnail(url=f"{self.DATA['img_url']}")
        else:
            embed.set_thumbnail(url=f"{self.USER.avatar_url}")
        embed.add_field(name=f"{self.NAME}", value=f"Lv.{self.LV}", inline=False)
        embed.add_field(name="[ HP ]", value=f"{self.showHP()}", inline=False)
        return embed

    def showHP(self):
        if self.HP <= 0:
            self.HP = 0
        rate = int((self.HP / self.MAX_HP * 100) // 10)
        return f"{rate * ':red_square:'}{(10-rate) * ':white_large_square:'}\n( {self.HP} / {self.MAX_HP} )"

class GAME:
    def __init__(self, p1, p2):
        self.ROUND = 0
        self.P1 = PLAYER(p1)
        self.P2 = PLAYER(p2)

    async def init(self, channel):
        self.channel = channel
        self.msg1 = await self.channel.send(embed=self.P2.showStatus())
        self.msg2 = await self.channel.send(embed=self.P1.showStatus())

    async def start(self):
        winner = None
        while self.ROUND <= 40:
            break
        return await self.channel.send(embed=self.end(winner))

    def end(self, winner):
        embed=discord.Embed(title="[ 전투 종료 ]", description="끝남.", color=0xe82626)
        return embed

##########################################################################################


class RPG(commands.Cog):
    def __init__(self, APP):
        self.APP = APP

    @commands.command(name="튜토리얼")
    async def Tutorial(self, ctx):
        await ctx.message.delete()
        user = load_Character(ctx.author.id)
        if not user:
            return await ctx.send("캐릭터부터 생성해주세요! $캐릭터 생성")
        
        if user['exp'] == 0:
            addPlayerEXP(ctx.author.id, 30)
        return await ctx.send("튜토리얼 끝!")
    @commands.group(name="캐릭터", pass_context=True)
    async def Character(self, ctx):
        await ctx.message.delete()
        if not ctx.invoked_subcommand is None:
            return 
        return await ctx.author.send(embed=HELP("캐릭터"))

    @Character.command(name="생성", pass_context=True)
    async def Character_Create(self, ctx):
        if load_Character(ctx.author.id):
            return await ctx.send("당신은 벌써 캐릭터가 생성되어 있습니다!")

        init_User(ctx.author)
        
        return await ctx.send("캐릭터 생성을 완료했습니다!")


    @commands.group(name="모험", pass_context=True)
    async def Adventure(self, ctx):
        await ctx.message.delete()
        if not ctx.invoked_subcommand is None:
            return
        return await ctx.author.send(embed=HELP("모험"))

    @Adventure.command(name="시작", pass_context=True)
    async def Adventure_Start(self, ctx):
        user = load_Character(ctx.author.id)
        user['info'] = ctx.author
        if not user:
            return await ctx.send("캐릭터부터 생성해주세요! $캐릭터 생성")
        elif not isGoPlace(user['exp']//30, "초원"):
            return await ctx.send("없는 장소거나 캐릭터의 레벨이 부족합니다!")

        ROOM = GAME(user, getMonster("초원", 1))   # 테스트용 
        #ROOM = GAME(user, getMonster(place, random.choices([1,2,3,4,5], weights=[45, 25, 15, 10, 5])))
        await ROOM.init(ctx.channel)
        
        return await ROOM.start()


    
def setup(APP):
    APP.add_cog(RPG(APP))