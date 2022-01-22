import asyncio, discord, os
import discord.ext.commands as commands
from discord.ext.commands import CommandNotFound, MissingRequiredArgument
from discord_slash import SlashCommand

intents = discord.Intents.all()
APP = commands.Bot(command_prefix="$", intents=intents)
slash = SlashCommand(APP, sync_commands=True, sync_on_cog_reload=True)
abs_cogs_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "Cogs")

for filename in os.listdir(abs_cogs_path):
    if filename.endswith(".py"):
        APP.load_extension(f"Cogs.{filename[:-3]}")

@APP.event
async def on_ready():
    print("다음으로 로그인합니다. : ")
    print(APP.user.name)
    print(APP.user.id)
    print("=============")
    game = discord.Game("퐁치 짝사랑")
    await APP.change_presence(status=discord.Status.online, activity=game)

@APP.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        return
    elif isinstance(error, MissingRequiredArgument):
        return await ctx.send("필요한 인자를 입력해주세요.")
    else:
        embed = discord.Embed(title="오류!!", description="오류가 발생했습니다.", color=0xFF0000)
        embed.add_field(name="상세", value=f"```{error}```")
        return await ctx.send(embed=embed)
        
@APP.command(name="reload")
async def reload(ctx, extension=None):
    if extension is None:
        for filename in os.listdir(abs_cogs_path):
            if filename.endswith(".py"):
                APP.unload_extension(f"Cogs.{filename[:-3]}")
                APP.load_extension(f"Cogs.{filename[:-3]}")
        return await ctx.send(":white_check_mark: 모든 Extension 을 리로드함.")
    else:
        try:
            APP.unload_extension(f"Cogs.{extension}")
            APP.load_extension(f"Cogs.{extension}")
        except Exception as e:
            return await ctx.send(f"{extension} 을 리로드할 수 없습니다.\n{e}")
        return await ctx.send(f":white_check_mark: {extension}을(를) 리로드함.")

f = open("C:\\Users\\PC\Desktop\\Casper\\Discord_Bot\\GGonnyang\\Ver2\\token.txt", "r")
token = f.readline()
f.close()
APP.run(token)