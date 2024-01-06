import discord

from discord.ext import commands
from discord.commands import slash_command
from discord.ui import View, Select

class Help(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.Cog.listener()
  async def on_ready(self):
    print(f"🟢 > Cog geladen: {__name__}")

  @slash_command(
    name="help",
    description="Benötigst du Hile zum Bot?"
  )
  async def help(self, ctx):
    await ctx.deafer()

    embedStart = discord.Embed(
      title="Hilfe zur Abseitsfalle",
      description="Benötigst du Hilfe zu den Bot-Commands? Wähle unter der Nachricht folgende Kategorien aus:",
      color=discord.Color.brand_green()
    )

    embedHelp = discord.Embed(
      description="Help-Commands",
      color=discord.Color.brand_green()
    ).add_field(
      name="_ _",
      value=f"""
        `> - /help` - Hol dir Hilfe zu allen Commands
        """
    )

    menu = Select(options=[
      discord.SelectOption(
        label="Help",
        value="menu_help",
        emoji="❓",
        description="Hier findest du Hilfe zum Bot"
      )
    ])

    async def menuAuswahl(interaction):
      if menu.value[0] == "menu_help":
        await message.edit(embed=embedHelp)

    menu.callback = menuAuswahl
    view = View(timeout=None)
    view.add_item(menu)

    message = await ctx.respond(embed=embedStart, view=view)
  
def setup(bot):
  bot.add_cog(Help(bot))