import discord

from discord.ext import commands
from discord.commands import slash_command, Option
from discord.ext.commands.errors import MissingPermissions, BotMissingPermissions, CommandOnCooldown
from datetime import timedelta

class Timeout(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  # Events
  @commands.Cog.listener()
  async def on_ready(self):
    print(f"🟢  > Cog geladen: {__name__}")

  # Commands
  @slash_command(name="timeout", description="Timeoute einen User")
  @commands.has_permissions(moderate_members=True)
  @commands.cooldown(1, 15, commands.BucketType.user)
  async def timeout(self, ctx, user: Option(discord.Member, required=True, description="Wer soll getimeoutet werden?"), reason: Option(str, required=True, description="Weshalb möchtest du ihn timouten?"), d: Option(int, max_value=30, description="Wie viele Tage soll er getimoutet werden?"), h: Option(int, description="Wie viele Stunden soll er getimoutet werden?"), m: Option(int, description="Wie viele Minuten soll er getimoutet werden?"), s: Option(int, description="Wie viele Sekunden soll er getimoutet werden?")):
    await ctx.defer()

    logchannel = discord.utils.get(ctx.guild.channels, name="「📃」adminlog")

    if user.id == ctx.author.id:
      embed = discord.Embed(
        title="`Error-04`",
        description="Du kannst dich nicht selbst Timeouten",
        color=discord.Color.brand_red()
      )
      await ctx.respond(embed=embed)
      return
    
    if user.guild_permissions.moderate_members:
      embed = discord.Embed(
        title="`Error-05`",
        description="Du kannst keinen Moderator Timeouten",
        color=discord.Color.brand_red()
      )
      await ctx.respond(embed=embed)
      return
    
    if d == None:
      d = 0
    if h == None:
      h = 0
    if m == None:
      m = 0
    if s == None:
      s = 0

    dur = timedelta(days=d, hours=h, minutes=m, seconds=s)

    await user.timeout_for(dur, reason=reason)

    embed = discord.Embed(
      title=":clock1: - Timeout!",
      description=f"**{user.name}** wurde von **{ctx.user.name}** getimeoutet.\n\n**Dauer**: {dur}\n**Grund:** {reason}",
      color=discord.Color.yellow()
    )
  
    await ctx.respond(embed=embed)
    await logchannel.send(embed=embed)

  # Error
  @timeout.error
  async def timeout_error(self, ctx, error):
    if isinstance(error, MissingPermissions):
      embed = discord.Embed(
        embed = discord.Embed(
          title="`Error-01`",
          description="Du hast nicht die benötigte(n) Berechtigung(en), um diesen Command nutzen zu dürfen.",
          color=discord.Color.brand_red()
        )
      )
      await ctx.respond(embed=embed)
      return
    
    elif isinstance(error, BotMissingPermissions):
      embed = discord.Embed(
        embed = discord.Embed(
          title="`Error-02`",
          description="Der Bot hat nicht die benötigte(n) Berechtigung(en), um diesen Command ausführen zu können.",
          color=discord.Color.brand_red()
        )
      )
      await ctx.respond(embed=embed)
      return
    
    elif isinstance(error, CommandOnCooldown):
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
  bot.add_cog(Timeout(bot))