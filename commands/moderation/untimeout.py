import discord

from discord.ext import commands
from discord.commands import slash_command, Option
from discord.ext.commands.errors import MissingPermissions, BotMissingPermissions, CommandOnCooldown
from datetime import datetime, timedelta

class Untimeout(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  # Events
  @commands.Cog.listener()
  async def on_ready(self):
    print(f"🟢  > Cog geladen: {__name__}")

  # Commands
  @slash_command(name="untimeout", description="Untimeoute einen User")
  @commands.has_permissions(moderate_members=True)
  @commands.cooldown(1, 15, commands.BucketType.user)
  async def untimeout(self, ctx, user: Option(discord.Member, required=True, description="Wer soll untimeouted werden?")):
    await ctx.defer()

    logchannel = discord.utils.get(ctx.guild.channels, name="「📃」adminlog")

    await user.remove_timeout()

    embed = discord.Embed(
      title=":unlock: - Untimeout!",
      description=f"**{user.name}** wurde von **{ctx.user.name}** untimeoutet.",
      color=discord.Color.yellow()
    )
  
    await ctx.respond(embed=embed)
    await logchannel.send(embed=embed)

  # Error
  @untimeout.error
  async def untimeout_error(self, ctx, error):
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
  bot.add_cog(Untimeout(bot))