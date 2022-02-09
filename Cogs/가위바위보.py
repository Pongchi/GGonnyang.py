import discord, asyncio, time, random
from discord_components import *
from discord.ext import commands


def showHP(HP, MAX_HP):
    if HP <= 0:
        HP = 0
    rate = int((HP / MAX_HP * 100) // 10)
    return f"{rate * ':red_square:'}{(10-rate) * ':white_large_square:'}\n( {HP} / {MAX_HP} )"

class PLAYER:
    def __init__(self, author):
        self.USER = author
        self.HP = 40
        self.MAX_HP = self.HP
        self.DAMAGE= 20
        self.RSP = ""

class GAME:
    def __init__(self, PLAYER1, PLAYER2):
        self.ROUND = 1
        self.PLAYER1 = PLAYER(PLAYER1)
        self.PLAYER2 = PLAYER(PLAYER2)
    
    def BROADCAST(self, content):
        embed=discord.Embed(title=f"[ {self.PLAYER1.USER.display_name} VS {self.PLAYER2.USER.display_name} ]", description=content, color=0x757bd7)
        embed.add_field(name=f"{self.PLAYER1.USER.display_name} 님의 체력", value=showHP(self.PLAYER1.HP, self.PLAYER1.MAX_HP), inline=False)
        embed.add_field(name=f"{self.PLAYER2.USER.display_name} 님의 체력", value=showHP(self.PLAYER2.HP, self.PLAYER2.MAX_HP), inline=False)
        embed.set_footer(text=f"현재 라운드 : {self.ROUND}")
        return embed

    def JUDGE(self):
        if self.PLAYER1.RSP == self.PLAYER2.RSP:
            return False
        else:
            if (self.PLAYER1.RSP == "가위" and self.PLAYER2.RSP == "보") or (self.PLAYER1.RSP == "바위" and self.PLAYER2.RSP == "가위") or (self.PLAYER1.RSP == "보" and self.PLAYER2.RSP == "바위"):
                return self.PLAYER1.USER
        return self.PLAYER2.USER
    
    def ATTACK(self, attacker, victim):
        victim.HP -= attacker.DAMAGE
        return f"{attacker.USER.mention} 님이 {victim.USER.mention} 님에게 {attacker.DAMAGE} 데미지를 주었습니다."
        
        

class RSP(commands.Cog):
    def __init__(self, APP):
        self.APP = APP

    @commands.Cog.listener()
    async def on_ready(self):
        return DiscordComponents(self.APP)

    @commands.command(name="가위바위보")
    async def RSP_Main(self, ctx):
        await ctx.message.delete()
        msg = await ctx.send(f"{ctx.author.mention} -> 상대를 기다리고있습니다...", components=[Button(label="가위바위보", style=ButtonStyle.green)])
        try:
            interaction = await self.APP.wait_for("button_click", check = lambda i: i.message.id == msg.id, timeout=20) #  and ctx.author != i.author
        except asyncio.TimeoutError:
            await msg.edit(content=f"{ctx.author.mention} -> 가위바위보 상대를 기다리다 지쳤습니다...")
            time.sleep(5)
            return await msg.delete()
        else:
            ROOM = GAME(ctx.author, interaction.author)
            await interaction.send("상대를 찾았습니다!!")

        while True:
            if ROOM.PLAYER1.HP <= 0 or ROOM.PLAYER2.HP <= 0:
                WINNER = ROOM.PLAYER1.USER if ROOM.PLAYER2.HP <= 0 else ROOM.PLAYER2.USER
                break
            await msg.edit(content="", embed=ROOM.BROADCAST("가위 / 바위 / 보 중에서 하나를 선택해주세요."), components=[[Button(label="가위", emoji="✌️", style=ButtonStyle.green), Button(label="바위", emoji="✊", style=ButtonStyle.blue), Button(label="보", emoji="✋", style=ButtonStyle.red)]])
            try:
                interaction1 = await self.APP.wait_for("button_click", check = lambda i: i.message.id == msg.id and (ROOM.PLAYER1.USER == i.author or ROOM.PLAYER2.USER == i.author), timeout=20)
                await interaction1.send(f"{interaction1.component.label} 을 선택하셨습니다.")
                interaction2 = await self.APP.wait_for("button_click", check = lambda i: i.message.id == msg.id and (ROOM.PLAYER1.USER == i.author or ROOM.PLAYER2.USER == i.author) and interaction1.author != i.author, timeout=20)
            except TimeoutError:
                return await msg.edit(embed=ROOM.BROADCAST("둘 중 한명이 선택을 안해서 게임이 종료되었습니다."))
            else:
                await interaction2.send(f"{interaction2.component.label} 을 선택하셨습니다.")
            
            if interaction1.author == ROOM.PLAYER1.USER:
                ROOM.PLAYER1.RSP = interaction1.component.label
                ROOM.PLAYER2.RSP = interaction2.component.label
            else:
                ROOM.PLAYER1.RSP = interaction2.component.label
                ROOM.PLAYER2.RSP = interaction1.component.label
                
                
            await msg.edit(embed=ROOM.BROADCAST(f"{ROOM.PLAYER1.USER.display_name} : {ROOM.PLAYER1.RSP}\n{ROOM.PLAYER2.USER.display_name} : {ROOM.PLAYER2.RSP}"))
            time.sleep(2)
            winner = ROOM.JUDGE()
            if not winner:
                await msg.edit(embed=ROOM.BROADCAST("서로 비겼기에 그냥 넘어갑니다."))
            else:
                if winner == ROOM.PLAYER1.USER:
                    await msg.edit(embed=ROOM.BROADCAST(ROOM.ATTACK(ROOM.PLAYER1, ROOM.PLAYER2)))
                else:
                    await msg.edit(embed=ROOM.BROADCAST(ROOM.ATTACK(ROOM.PLAYER2, ROOM.PLAYER1)))
            
            ROOM.ROUND += 1
            time.sleep(2)
            
            
        return await msg.edit(embed=ROOM.BROADCAST(f"승자 : {WINNER.mention}"))

def setup(APP):
    APP.add_cog(RSP(APP))
