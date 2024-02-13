import discord
import aiosqlite
import asyncio

from discord.ext import commands
from discord.commands import slash_command, Option
from discord.ext.commands.errors import MissingPermissions, BotMissingPermissions, CommandOnCooldown

from checks.ticket import remove_ticket

class Close(commands.Cog):
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
  @slash_command(name="ticket-close", description="Banne einen User")
  @commands.has_permissions(manage_channels=True)
  @commands.cooldown(1, 5, commands.BucketType.user)
  async def close(self, ctx):
    await ctx.defer()

    logchannel = discord.utils.get(ctx.guild.channels, name="「📃」adminlog")
    
    embedC = discord.Embed(
      title=":wastebasket: - Ticket geschlossen!",
      description="Das Ticket wird in **10 Sekunden geschlossen!**",
      color=discord.Color.dark_red()
    )

    embedL = discord.Embed(
      title=":wastebasket: - Ticket geschlossen!",
      description=f"Das Ticket **{ctx.channel.name}** wurde geschlossen!",
      color=discord.Color.dark_red()
    ).set_footer(
      text=ctx.channel.name
    )

    await remove_ticket(ctx.channel.id)

    await ctx.respond(embed=embedC)
    await asyncio.sleep(10)
    await ctx.channel.delete()
    await logchannel.send(embed=embedL)

  # Error
  @close.error
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
  bot.add_cog(Close(bot))