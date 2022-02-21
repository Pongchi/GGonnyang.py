import discord, time, random
from discord.ext import commands, tasks

# 발표 랜덤 순서, 발표 시간 알림
class Casper(commands.Cog):
    def __init__(self, APP):
        self.APP = APP
        self.presenter = []
        self.seq = -1
        self.cnt = 0
    
    @tasks.loop(minutes=1.0)
    async def Countdown(self, ctx):
        await ctx.send(f"발표 시간이 {self.cnt}분 경과했습니다.")
        self.cnt += 1

    def SeqEmbed(self):
        if len(self.presenter):
            description = "\n".join([f"{i + 1}. {user.mention}" for i, user in enumerate(self.presenter)])
            embed = discord.Embed(
                title=f"총 인원 : {len(self.presenter)}명",
                description=description)
        
        else:
            embed = discord.Embed(title=f"사람도 없는데 순서는 무슨!")

        if self.seq >= 0:
            embed.set_author(name=f"현재 발표자 : {self.presenter[self.seq].display_name}", icon_url=self.presenter[self.seq].avatar_url)

        return embed

    @commands.command(name="발표")
    async def Presentation(self, ctx, seq=None):
        if seq == "순서":
            if not len(self.presenter):
                return await ctx.send("발표 순서를 먼저 정해주세요!")
            return await ctx.send(content=f"이번 발표는 {self.presenter[self.seq].mention} 입니다.", embed=self.SeqEmbed())
        elif seq == "시작":
            if not self.Countdown.is_running:
                return await ctx.send("벌써 누가 발표를 하고있습니다. 다른 사람의 발표를 끝내고 시작해주세요.")
            elif not len(self.presenter):
                return await ctx.send("발표 순서를 먼저 정해주세요!")
            
            self.cnt = 0
            await ctx.send(f"발표를 시작합니다! 이번 발표는 {self.presenter[self.seq].mention} 입니다.")
            return self.Countdown.start(ctx)
        elif seq == "끝":
            self.cnt = 0
            await ctx.send("발표 알람을 종료했습니다.")
            return self.Countdown.cancel()
        elif seq == "다음" and self.seq < len(self.presenter)-1:
            self.seq += 1
            return await ctx.send(f"이번 발표는 {self.presenter[self.seq]} 입니다.")
        elif seq == "초기화":
            if not self.Countdown.is_running():
                self.Countdown.cancel()
            self.req = -1
            self.presenter = []
            return await ctx.send("발표자를 초기화했습니다.")
        elif seq != '순서정하기':
            return

        self.presenter = []
        embed=discord.Embed(title="발표 순서정하기", description=": 발표를 하시는 분들은 따봉 버튼을 눌러주세요!", color=0xb62525)
        embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/528/528108.png")
        embed.set_footer(text="For Casper")
        msg = await ctx.send(embed=embed)
        await msg.add_reaction("👍")

        time.sleep(8)
        msg = await msg.channel.fetch_message(msg.id)
        for reaction in msg.reactions:
            if not reaction.emoji == "👍":
                continue
            async for user in reaction.users():
                if user.bot:
                    continue
                self.presenter.append(user)
        
        if len(self.presenter) >= 1:
            self.seq = 0

        await msg.delete()
        msg = await ctx.send("랜덤을 몇번 돌릴까요? 사용법: 랜덤 <숫자>")
        cntMsg = await self.APP.wait_for('message', check=lambda message: message.content.startswith("랜덤 ") and len(message.content) >= 4, timeout=10)
        cnt = 5 if int(cntMsg.content[3:]) > 5 else int(cntMsg.content[3:])
        await cntMsg.delete()

        for i in range(cnt-1):
            random.shuffle(self.presenter)
            await ctx.send(embed=self.SeqEmbed())

        await msg.delete()
        return await ctx.send(embed=self.SeqEmbed())

def setup(APP):
    APP.add_cog(Casper(APP))