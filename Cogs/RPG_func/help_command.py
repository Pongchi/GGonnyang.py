import discord

def HELP(cmd):
    embed=discord.Embed(title="[ RPG 도움말 ]", description="- [] 는 없어도 되는 인자. <>는 꼭 필요한 인자. | 는 '이거나' 라는 뜻.", color=0xe82626)
    if cmd == "캐릭터" or "모두":
        embed.add_field(name="```[ 캐릭터 관련 명령어 ]```", inline=False)
        embed.add_field(name="$캐릭터", value="- 캐릭터 명령어에 대한 명령어들을 봅니다.", inline=False)
        embed.add_field(name="$캐릭터 생성", value="- 캐릭터가 없다면 자신의 캐릭터를 생성합니다.", inline=False)
        embed.add_field(name="$캐릭터 정보 [유저ID]", value="- [유저ID]의 캐릭터 정보를 불러옵니다. 기본값은 자신의 ID", inline=False)

    return embed