import discord

from discord.ext import commands
from discord.commands import slash_command
from discord.ui import View, Select
from datetime import datetime

class Help(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  # Events
  @commands.Cog.listener()
  async def on_ready(self):
    print(f"🟢 > Cog geladen: {__name__}")
  
  # Commands
  help = discord.SlashCommandGroup(name="help", description="Hilfecommands")

  @slash_command(name="helpmenu", description="Hier findest du das gesamte Help-Menu")
  @commands.cooldown(1, 5)
  async def helpmenu(self, ctx):
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

  @help.command(name="help", description="Hilfe zu den Hilfe-Commands")
  @commands.cooldown(1, 5)
  async def help_help(self, ctx):
    await ctx.defer()
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
    await ctx.respond(embed=embedHelp)
    return
  
  @help.command(name="sonstiges", description="Hilfe zu den Sonstigen Commands")
  @commands.cooldown(1, 5)
  async def help_misc(self, ctx):
    await ctx.defer()
    embedMisc = discord.Embed(
      description="Sonstige Commands",
      color=discord.Color.brand_green()
    ).add_field(
      name="_ _",
      value=f"""
        > - `/transfer` - Erstelle neue Transfernachrichten
        """
    )
    await ctx.respond(embed=embedMisc)
    return

  
def setup(bot):
  bot.add_cog(Help(bot))