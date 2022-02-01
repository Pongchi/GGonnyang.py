import discord, pymysql, json
from discord.ext import commands

con = pymysql.connect(host='localhost', user="root", password="1219", db="GGonnyang", charset="utf8")
cursor = con.cursor(pymysql.cursors.DictCursor)

######################################################################################
def getData(type, no):
    if type == "pokemon":
        SQL = "SELECT * FROM Pokemon WHERE no=%s"
        cursor.execute(SQL, (no))
        return cursor.fetchone()
    with open(f".\\Cogs\\TRAINER\\{no}.json", "rt", encoding="UTF8") as f:
            return json.load(f)

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

    @Pokemon.command(name="스타터포켓몬")
    async def Pokemon_Starting(self, ctx):
        return await ctx.send("스타터 포켓몬 선택")
    
def setup(APP):
    APP.add_cog(POKEMON_GAME(APP))