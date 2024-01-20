import discord

from discord.ext import commands
from discord.commands import slash_command
from discord.ui import View, Select
from datetime import datetime
from discord.ext.commands.errors import CommandOnCooldown

class Help(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  # Events
  @commands.Cog.listener()
  async def on_ready(self):
    print(f"🟢  > Cog geladen: {__name__}")
  
  # Commands
  @slash_command(name="help", description="Hier findest du das gesamte Help-Menu")
  @commands.cooldown(1, 15, commands.BucketType.user)
  async def help(self, ctx):
    await ctx.defer()

    embedStart = discord.Embed(
      title="Hilfe zur Abseitsfalle",
      description="Benötigst du Hilfe zu den Bot-Commands? Wähle unter der Nachricht folgende Kategorien aus:",
      color=discord.Color.brand_green()
    )

    embedHelp = discord.Embed(
      description="Hilfe Commands",
      color=discord.Color.brand_green()
    ).add_field(
      name="_ _",
      value=f"""
        > - `/helpmenu`       - Hirr findest du das gesamte Help-Menü
        > - `/help help`      - Hilfe zu den Hilfe-Commands
        > - `/help sonstiges` - Hilfe zu den Sontigen Commands
        """
    )

    embedMisc = discord.Embed(
      description="Sonstige Commands",
      color=discord.Color.brand_green()
    ).add_field(
      name="_ _",
      value=f"""
        > - `/transfer` - Erstelle neue Transfernachrichten
        """
    )
    menu = Select(options=[
      discord.SelectOption(label="Menu", value="menu_start", emoji="👋🏻", description="Help-Menü"),
      discord.SelectOption(label="Help", value="menu_help", emoji="❓", description="Hier findest du Hilfe zum Bot"),
      discord.SelectOption(label="Sonstiges", value="menu_misc", emoji="👀", description="Hier findest du den sonstigen Commands")
    ])

    async def menuAuswahl(interaction):
      if menu.values[0] == "menu_start":
        await message.edit(embed=embedStart)
      if menu.values[0] == "menu_help":
        await message.edit(embed=embedHelp)
      if menu.values[0] == "menu_misc":
        await message.edit(embed=embedMisc)

    menu.callback = menuAuswahl
    view = View(timeout=None)
    view.add_item(menu)

    message = await ctx.respond(embed=embedStart, view=view)

  # Error
  @help.error
  async def help_error(self, ctx, error):    
    if isinstance(error, CommandOnCooldown):
      embed = discord.Embed(
        embed = discord.Embed(
          title="`Error-03`",
          description="Der Command befindet sich noch immer im Cooldown.",
          color=discord.Color.brand_red()
        )
      )
      await ctx.respond(embed=embed)
      return
  
def setup(bot):
  bot.add_cog(Help(bot))