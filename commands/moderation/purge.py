import discord

from discord.ext import commands
from discord.commands import slash_command, Option
from discord.ext.commands.errors import MissingPermissions, BotMissingPermissions, CommandOnCooldown

class Purge(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  # Events
  @commands.Cog.listener()
  async def on_ready(self):
    print(f"🟢  > Cog geladen: {__name__}")

  # Commands
  @slash_command(name="purge", description="Lösche mehrere Nachrichten aufeinmal")
  @commands.has_permissions(manage_messages=True)
  @commands.cooldown(1, 5, commands.BucketType.user)
  async def purge(self, ctx, anzahl: Option(int, required=True, description="Wie viele Nachrichten möchtest du löschen?")):
    await ctx.defer()

    logchannel = discord.utils.get(ctx.guild.channels, name="「📃」adminlog")

    anz = await ctx.channel.purge(limit=anzahl+1)

    embed = discord.Embed(
      title=":wastebasket: - Nachrichten gelöscht!",
      description=f"**{ctx.user.name}** hat **{len(anz)} Nachrichten** in <#{ctx.channel.id}> gelöscht!",
      color=discord.Color.red()
    )

    await ctx.channel.send(embed=embed)
    await logchannel.send(embed=embed)

  # Error
  @purge.error
  async def purge_error(self, ctx, error):
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
  bot.add_cog(Purge(bot))