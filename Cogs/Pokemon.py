import discord, pymysql, json, asyncio
from discord.ext import commands
from discord_components import *
from collections import OrderedDict

con = pymysql.connect(host='localhost', user="root", password="1219", db="GGonnyang", charset="utf8")
cursor = con.cursor(pymysql.cursors.DictCursor)

######################################################################################
def Select_Trainer(id):
    SQL = "SELECT * FROM Trainer WHERE id=%s"
    cursor.execute(SQL, (id))
    return cursor.fetchone()

def getData(type, no):
    if type == "pokemon":
        SQL = "SELECT * FROM Pokemon WHERE no=%s"
        cursor.execute(SQL, (no))
        return cursor.fetchone()
    with open(f".\\Cogs\\POKEMON\\TRAINER\\{no}.json", "rt", encoding="UTF8") as f:
            return json.load(f)

def init_User(author, pokemon):
    SQL = "INSERT INTO Trainer (id, money) VALUES (%s, %s)"
    cursor.execute(SQL, (author.id, 1000))
    con.commit()

    user_data = OrderedDict()
    user_data['nickname'] = author.display_name
    user_data['Select_Pokemon'] = pokemon
    user_data['Pokemons'] = {}
    user_data['Inventory'] = {'도구':0, '물약':0}
    
    with open(f'.\\Cogs\\POKEMON\\TRAINER\\{author.id}.json', 'w', encoding='utf-8') as make_file:
        json.dump(user_data, make_file, ensure_ascii=False, indent="\t")
    return 0

def SELECT_STARTING_EMBED(list):
    embed=discord.Embed(title="[ 스타팅포켓몬 선택 ]", color=0xe21818)
    for _type in list:
        embed.add_field(name=f"타입 : {_type}", inline=False)
        for pokemon in list[_type]:
            embed.add_field(name=f"{pokemon.name}", value="설명 : {pokemon.description}", inline=False)
    return embed

async def SELECT_STARTING(ctx):
    with open(f".\\Cogs\\POKEMON\\Starting_Pokemons.json", "rt", encoding="UTF8") as f:
            starting = json.load(f)
    STARTING = [[], [], []]
    msg = await msg.send(embed=SELECT_STARTING_EMBED(starting), components=STARTING)
    try:
        interaction = await self.APP.wait_for("button_click", check = lambda i: ctx.author == i.author, timeout=60)
    except asyncio.TimeoutError:
        await msg.edit(content="60초동안 아무 반응이 없어 스타팅포켓몬 연결이 종료되었습니다. 다시 스타팅 포켓몬을 선택해주세요.")
        return False
    else:
        await interaction.edit_origin(content=f"{interaction.component.label} 을 선택하셨습니다!")

    return interaction.component.label
######################################################################################
class TRAINER:
    def __init__(self, info):
        self.ID = info['id']
        self.DATA = getData("trainer", info['id'])
        self.POKEMON = POKEMON(self.DATA['Pokemons'][self.DATA['Select_Pokemon']])
        del self.DATA['Pokemons']
        
class POKEMON:
    def __init__(self, info):
        self.NO = info['No']
        self.LV = info['Lv']
        self.NAME = info['Name']
        self.ATTR1 = info['Attr1']
        self.ATTR2 = info['Attr2']
        self.DATA = getData('pokemon', info['No'])
        self.HP = (((self.DATA['HP'] * 2) + info['Stat']['HP']) * self.LV/100) + 10 + self.LV
        self.MAX_HP = self.HP
        self.STR = (((self.DATA['STR'] * 2) + info['Stat']['STR']) * self.LV) + 5
        self.DEF = (((self.DATA['DEF'] * 2) + info['Stat']['DEF']) * self.LV) + 5
        self.SSTR = (((self.DATA['SSTR'] * 2) + info['Stat']['SSTR']) * self.LV) + 5
        self.SDEF = (((self.DATA['DEF'] * 2) + info['Stat']['SDEF']) * self.LV) + 5
        self.DEX = (((self.DATA['DEX'] * 2) + info['Stat']['DEX']) * self.LV) + 5
######################################################################################
class POKEMON_GAME(commands.Cog):
    def __init__(self, APP):
        self.APP = APP
        
    @commands.group(name="포켓몬")
    async def Pokemon(self, ctx):
        await ctx.message.delete()
        if not ctx.invoked_subcommand is None:
            return
        return await ctx.send("도움말.")

    @Pokemon.command(name="스타팅포켓몬")
    async def Pokemon_Starting(self, ctx):
        if Select_Trainer(ctx.author.id):
            return await ctx.send("너는 벌써 받았다구!")

        selecting = await SELECT_STARTING(ctx)
        if not selecting:
            return
        
        init_User(ctx.author, selecting)
        return awaix msg.edit(content="포켓몬 세계에 오신 것을 환영합니다.")
    
def setup(APP):
    APP.add_cog(POKEMON_GAME(APP))