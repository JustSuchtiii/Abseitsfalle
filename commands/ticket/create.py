import discord
import aiosqlite

from discord.ext import commands
from discord.commands import slash_command, Option
from discord.ext.commands.errors import MissingPermissions, BotMissingPermissions, CommandOnCooldown
from discord.ui import View, Button, Select
from random import randint

from checks.ticket import add_ticket

class Create(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.DB = "db/tickets.db"

  # Events
  @commands.Cog.listener()
  async def on_ready(self):
    async with aiosqlite.connect(self.DB) as db:
      await db.execute(
        """
        CREATE TABLE IF NOT EXISTS tickets (
        channel_id INTEGER PRIMARY KEY,
        ticket_id INTEGER UNIQUE,
        guild_id INTEGER DEFAULT 1087465763125862490,
        user_id INTEGER DEFAULT 0,
        version INTEGER DEFAULT 0
        )"""
      )
    print(f"🟢  > Cog geladen: {__name__}")


  # Commands
  @slash_command(name="ticket-create", description="Erstell dir ein Ticket")
  @commands.cooldown(1, 5, commands.BucketType.user)
  async def create(self, ctx):
    await ctx.defer()

    logchannel = discord.utils.get(ctx.guild.channels, name="「📃」adminlog")

    guild = ctx.guild
    role = discord.utils.get(guild.roles, name="「🔧」Team")

    overwrites = {
      guild.default_role: discord.PermissionOverwrite(view_channel=False),
      ctx.user: discord.PermissionOverwrite(view_channel=True, manage_channels=True),
      role: discord.PermissionOverwrite(view_channel=True)
    }

    select = Select(options=[
      discord.SelectOption(label="Support Ticket", value="T1", emoji="🎫", description="Erstelle ein Support Ticket"),
      discord.SelectOption(label="Partner Ticket", value="T2", emoji="🤝", description="Erstelle ein Partner Ticket"),
      discord.SelectOption(label="Bewerbungs Ticket", value="T3", emoji="📝", description="Erstelle ein Bewerbungs Ticket")
    ])

    async def ticketCallback(interaction):
      if select.values[0] == "T1":
        category = discord.utils.get(guild.categories, name="「🎟」Tickets")
        numbT = randint(1, 9999)
        if numbT <= 999 and numbT >= 100:
          numbT = str(f"0{numbT}")
        elif numbT <= 99 and numbT >= 10:
          numbT = str(f"00{numbT}")
        elif numbT <= 9:
          numbT = str(f"000{numbT}")
        
        channel = await ctx.guild.create_text_channel(f"ticket-{numbT}", category=category, overwrites=overwrites)
        await add_ticket(ctx.guild.id, channel.id, numbT, ctx.author.id, 1)

        embedC = discord.Embed(
          title=":ticket: - Ticket erstellt!",
          description=f"Es wurde ein neues Ticket erstellt: <#{channel.id}>",
          color=discord.Color.dark_green()
        ).set_footer(
          text=ctx.channel.name
        )

        embedT = discord.Embed(
          description="Herzlich Willkommen im Ticket-Support. Schreibe hier dein Anliegen rein. Das Team wird in kürze zur verfügung stehen.",
          color=discord.Color.greyple()
        )

        await interaction.response.send_message(embed=embedC, ephemeral=True)
        await channel.edit(topic=interaction.user.id)
        await channel.send("<@&1106135363640098836>", embed=embedT)
        await logchannel.send(embed=embedC)

      elif select.values[0] == "T2":
        category = discord.utils.get(guild.categories, name="「🤝」Partner")
        numbT = randint(1, 9999)
        if numbT <= 999 and numbT >= 100:
          numbT = str(f"0{numbT}")
        elif numbT <= 99 and numbT >= 10:
          numbT = str(f"00{numbT}")
        elif numbT <= 9:
          numbT = str(f"000{numbT}")
        
        channel = await ctx.guild.create_text_channel(f"partner-{numbT}", category=category, overwrites=overwrites)
        await add_ticket(ctx.guild.id, channel.id, numbT, ctx.author.id, 2)

        embedC = discord.Embed(
          title=":ticket: - Ticket erstellt!",
          description=f"Es wurde ein neues Ticket erstellt: <#{channel.id}>",
          color=discord.Color.dark_green()
        ).set_footer(
          text=ctx.channel.name
        )

        embedT = discord.Embed(
          description="Herzlich Willkommen in der Partnerschafts-Anfrage. Die Server-Leitung wird in kürze zur verfügung stehen.",
          color=discord.Color.greyple()
        )

        await interaction.response.send_message(embed=embedC, ephemeral=True)
        await channel.edit(topic=interaction.user.id)
        await channel.send("<@&1106120840669573172>", embed=embedT)
        await logchannel.send(embed=embedC)

      elif select.values[0] == "T3":
        embedC = discord.Embed(
          description=":x: Es konnte kein Bewerbungsticket erstellt werden, da aktuell keine Bewerbungsphase ist.",
          color=discord.Color.red()
          )
        #await interaction.response.send_message(embed=embed1)
        #category = discord.utils.get(guild.categories, name="「🤝」Bewerbungen")
        #numbT = randint(1, 9999)
        #if numbT <= 999 and numbT >= 100:
        #  numbT = str(f"0{numbT}")
        #elif numbT <= 99 and numbT >= 10:
        #  numbT = str(f"00{numbT}")
        #elif numbT <= 9:
        #  numbT = str(f"000{numbT}")
        
        #channel = await ctx.guild.create_text_channel(f"bew-{numbT}", category=category, overwrites=overwrites)
        #await add_ticket(ctx.guild.id, channel.id, numbT, ctx.author.id, 3)

        #embedC = discord.Embed(
        #  title=":ticket: - Ticket erstellt!",
        #  description=f"Es wurde ein neues Ticket erstellt: <#{channel.id}>",
        #  color=discord.Color.dark_green()
        #).set_footer(
        #  text=ctx.channel.name
        #)

        #embedT = discord.Embed(
        #  description="Herzlich Willkommen in der Bewerber-Anfrage. Die Server-Leitung wird in kürze zur verfügung stehen.",
        #  color=discord.Color.greyple()
        #)

        await interaction.response.send_message(embed=embedC, ephemeral=True)
        #await logchannel.send(embed=embedC)
        #await channel.edit(topic=interaction.user.id)
        #await channel.send("<@&1106120840669573172>", embed=embedT)

    select.callback = ticketCallback
    view = View(timeout=None)
    view.add_item(select)
    embed = discord.Embed(
      description="Was für ein Ticket möchtest du erstellen:",
      color=discord.Color.yellow()
    )

    await ctx.respond(embed=embed, ephemeral=True, view=view)

  # Error
  @create.error
  async def create_error(self, ctx, error):
    if isinstance(error, MissingPermissions):
      embed = discord.Embed(
        title="`Error-01`",
        description="Du hast nicht die benötigte(n) Berechtigung(en), um diesen Command nutzen zu dürfen.",
        color=discord.Color.brand_red()
      )
      await ctx.respond(embed=embed)
      return
    
    elif isinstance(error, BotMissingPermissions):
      embed = discord.Embed(
        title="`Error-02`",
        description="Der Bot hat nicht die benötigte(n) Berechtigung(en), um diesen Command ausführen zu können.",
        color=discord.Color.brand_red()
      )
      await ctx.respond(embed=embed)
      return
    
    elif isinstance(error, CommandOnCooldown):
      embed = discord.Embed(
        title="`Error-03`",
        description="Der Command befindet sich noch immer im Cooldown.",
        color=discord.Color.brand_red()
      )
      await ctx.respond(embed=embed)
      return
  
def setup(bot):
  bot.add_cog(Create(bot))