import discord

from discord.ext import commands
from discord.commands import slash_command, Option
from discord.ext.commands.errors import MissingPermissions, BotMissingPermissions, CommandOnCooldown

class Ban(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  # Events
  @commands.Cog.listener()
  async def on_ready(self):
    print(f"🟢  > Cog geladen: {__name__}")

  # Commands
  @slash_command(name="ban", description="Banne einen User")
  @commands.has_permissions(ban_members=True)
  @commands.cooldown(1, 15, commands.BucketType.user)
  async def ban(self, ctx, user: Option(discord.Member, required=True, description="Wen möchtest du bannen?"), reason: Option(str, required=True, description="Weshalb möchtest du ihn bannen?")):
    await ctx.defer()

    logchannel = discord.utils.get(ctx.guild.channels, name="「📃」adminlog")

    if user.id == ctx.author.id:
      embed = discord.Embed(
        title="`Error-04`",
        description="Du kannst dich nicht selbst bannen.",
        color=discord.Color.brand_red()
      )
      await ctx.respond(embed=embed)
      return
    
    if user.guild_permissions.moderate_members:
      embed = discord.Embed(
        title="`Error-05`",
        description="Du kannst keinen Moderator bannen.",
        color=discord.Color.brand_red()
      )
      await ctx.respond(embed=embed)
      return
    
    await user.ban(reason=reason)
    
    embed = discord.Embed(
      title=":man_police_officer: - User gebannt!",
      description=f"**{user.name}** wurde von **{ctx.user.name}** gebannt.\n\n**Grund:** {reason}",
      color=discord.Color.red()
    )

    await ctx.channel.send(embed=embed)
    await logchannel.send(embed=embed)

  # Error
  @ban.error
  async def ban_error(self, ctx, error):
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
  bot.add_cog(Ban(bot))