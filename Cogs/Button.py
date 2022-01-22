from discord_components import *
from discord.ext import commands

class BTN(commands.Cog):
    def __init__(self, APP):
        self.APP = APP

    @commands.Cog.listener()
    async def on_ready(self):
        return DiscordComponents(self.APP)

    @commands.command(name="버튼")
    async def btn(self, ctx):
        await ctx.send("hello", components = [Button(label="click me!!", style=ButtonStyle.blue)])
        interaction = await self.APP.wait_for("button_click", check = lambda i: i.component.label.startswith("click"))
        return await interaction.respond(content = "Button clicked!", ephemeral=False)

def setup(APP):
    APP.add_cog(BTN(APP))