import discord

from discord.ext import commands
from discord.commands import slash_command, Option
from discord.ext.commands.errors import MissingPermissions, BotMissingPermissions, CommandOnCooldown

class Kick(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  # Events
  @commands.Cog.listener()
  async def on_ready(self):
    print(f"🟢  > Cog geladen: {__name__}")

  # Commands
  @slash_command(name="kick", description="Kicke einen User")
  @commands.has_permissions(kick_members=True)
  @commands.cooldown(1, 5, commands.BucketType.user)
  async def kick(self, ctx, user: Option(discord.Member, required=True, description="Wen möchtest du kicken?"), reason: Option(str, required=True, description="Weshalb möchtest du ihn kicken?")):
    await ctx.defer()

    logchannel = discord.utils.get(ctx.guild.channels, name="「📃」adminlog")
    
    if user.id == ctx.author.id:
      embed = discord.Embed(
        title="`Error-04`",
        description="Du kannst dich nicht selbst kicken.",
        color=discord.Color.brand_red()
      )
      await ctx.respond(embed=embed)
      return
    
    if user.guild_permissions.moderate_members:
      embed = discord.Embed(
        title="`Error-05`",
        description="Du kannst keinen Moderator kicken.",
        color=discord.Color.brand_red()
      )
      await ctx.respond(embed=embed)
      return
    
    await user.kick(reason=reason)
    
    embed = discord.Embed(
      title=":man_police_officer: - User gekickt!",
      description=f"**{user.name}** wurde von **{ctx.user.name}** gekickt.\n\n**Grund:** {reason}",
      color=discord.Color.red()
    )

    await ctx.channel.send(embed=embed)
    await logchannel.send(embed=embed)

  # Error
  @kick.error
  async def kick_error(self, ctx, error):
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
  bot.add_cog(Kick(bot))