import discord, asyncio, time
from discord_components import *
from discord.ext import commands
########################################################################################################################################################################################
def HELP(author):
        embed=discord.Embed(title="[ 결투 도움말 ]", description="- [] 는 없어도 되는 인자. <>는 꼭 필요한 인자. | 는 '이거나' 라는 뜻.", color=0xe82626)
        embed.add_field(name="$결투 시작", value="- 플레이어 2명이서 생사결투를 벌입니다!", inline=False)
        embed.set_author(name=author.display_name, icon_url=author.avatar_url)
        return embed

def showHP(HP, MAX_HP):
    if HP <= 0:
        HP = 0
    rate = int((HP / MAX_HP * 100) // 10)
    return f"{rate * ':red_square:'}{(10-rate) * ':white_large_square:'}\n( {HP} / {MAX_HP} )"
########################################################################################################################################################################################
class PLAYER:
    def __init__(self, author):
        self.USER = author
        self.HP = 40
        self.MAX_HP = self.HP
        self.DAMAGE = 5

    def Status(self):
        embed=discord.Embed(title=f"[ 상태창 : {self.USER.display_name} ]", description=showHP(self.HP, self.MAX_HP), color=0x757bd7)
        embed.set_author(name=self.USER.display_name, icon_url=self.USER.avatar_url)
        return embed

    def ACTION(self):
        return "ATTACK"

class GAME:
    def __init__(self, PLAYER1, PLAYER2):
        self.ROUND = 1
        self.PLAYER1 = PLAYER(PLAYER1)
        self.PLAYER2 = PLAYER(PLAYER2)

    def ATTACK(self, attacker, victim):
        victim.HP -= attacker.DAMAGE
        return f"{attacker.USER.mention} 님이 {victim.USER.mention} 님에게 {attacker.DAMAGE} 데미지를 주었습니다."

    def BROADCAST(self, content):
        embed=discord.Embed(title=f"[ {self.PLAYER1.USER.display_name} VS {self.PLAYER2.USER.display_name} ]", description=content, color=0x757bd7)
        embed.set_footer(text=f"현재 라운드 : {self.ROUND}")
        return embed


########################################################################################################################################################################################
class PVP(commands.Cog):
    def __init__(self, APP):
        self.APP = APP

    @commands.Cog.listener()
    async def on_ready(self):
        return DiscordComponents(self.APP)

    @commands.group(name="결투")
    async def PVP_Main(self, ctx):
        if not ctx.invoked_subcommand is None:
            return
        return await ctx.send(embed=HELP(ctx.author))
    
    @PVP_Main.command(name="시작")
    async def PVP_Start(self, ctx):
        await ctx.message.delete()
        msg = await ctx.send(f"{ctx.author.mention} -> 결투 상대를 기다리고있습니다...", components=[Button(label="참가하기", style=ButtonStyle.green)])
        try:
            interaction = await self.APP.wait_for("button_click", check = lambda i: i.message.id == msg.id, timeout=20) #  and ctx.author != i.author
        except asyncio.TimeoutError:
            await msg.edit(content=f"{ctx.author.mention} -> 결투 상대를 기다리다 지쳤습니다...")
            time.sleep(5)
            return await msg.delete()
        else:
            await interaction.edit_origin(content=f"[ 결투 매치 성공 ] PLAYER1:{ctx.author.mention} VS PLAYER2:{interaction.author.mention}\n- 게임 환경을 설정중입니다. 잠시만 기다려주세요.")
            ROOM = GAME(ctx.author, interaction.author)
            msg_player1 = await ctx.send(embed=ROOM.PLAYER1.Status())
            msg_broadcast = await ctx.send(embed=ROOM.BROADCAST("이 메시지는 게임 상황을 알려주는 메시지입니다."))
            msg_player2 = await ctx.send(embed=ROOM.PLAYER2.Status())
            
        await msg_broadcast.edit(embed=ROOM.BROADCAST("게임 환경 설정 완료!!"))
        await msg.delete()
        ######################################################
        while True:
            if ROOM.PLAYER1.HP <= 0 or ROOM.PLAYER2.HP <= 0:
                WINNER = ROOM.PLAYER1.USER if ROOM.PLAYER2.HP <= 0 else ROOM.PLAYER2.USER
                break
            
            if ROOM.ROUND % 2 == 1:
                await msg_broadcast.edit(embed=ROOM.BROADCAST(ROOM.ATTACK( ROOM.PLAYER1, ROOM.PLAYER2 )))
            else:
                await msg_broadcast.edit(embed=ROOM.BROADCAST(ROOM.ATTACK( ROOM.PLAYER2, ROOM.PLAYER1 )))

            await msg_player1.edit(embed=ROOM.PLAYER1.Status())
            await msg_player2.edit(embed=ROOM.PLAYER2.Status())

            ROOM.ROUND += 1
            time.sleep(1)
        ######################################################
        await msg_player1.delete()
        await msg_player2.delete()
        return await msg_broadcast.edit(embed=ROOM.BROADCAST(f"승자 : {WINNER.mention}"))

def setup(APP):
    APP.add_cog(PVP(APP))