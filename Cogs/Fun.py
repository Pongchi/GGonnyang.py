import random, time, asyncio
from discord.ext import commands
from discord_components import *

class Fun(commands.Cog):
    def __init__(self, APP):
        self.APP = APP
        
    @commands.command(name="순발력")
    async def Alacrity(self, ctx):
        msg = await ctx.send("순발력 테스트!", components=[[Button(label="👍")]])
        time.sleep(3)
        while True:
            if random.randint(1, 2) == 2:
                await msg.edit(content="{}".format(random.choice(["ㅋㅋㄹㅃㅃ", "낚였냐?", "누르면 안된다구!!", "ㅋ?", "지금 눌지마!!"])))
                try:
                    timeout = random.randint(0, 9) + random.random()
                    await msg.edit(components=[[Button(label="👍")]])
                    interaction = await self.APP.wait_for("button_click", check = lambda i: i.component.label == "👍", timeout=timeout)
                except asyncio.TimeoutError:
                    continue
                else:
                    return await msg.edit(content=f"{interaction.author.name} 가 누르면 안되는데 눌러버림!!")
            else:
                break

        await msg.edit(content="지금 눌러!!")
        t1 = time.time()
        interaction = await self.APP.wait_for("button_click", check = lambda i: i.component.label == "👍", timeout=10)
        t2 = time.time()
        await interaction.send("너가 젤 빨랐음!!")
        return await msg.edit(content=interaction.author.name + "님이 젤 빨랐음!!! - 반응속도 : " + str(t2 - t1))

def setup(APP):
    APP.add_cog(Fun(APP))