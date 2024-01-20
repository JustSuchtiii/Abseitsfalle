import discord

from discord.ext import commands
from discord.commands import slash_command, Option
from discord.ext.commands.errors import MissingPermissions, BotMissingPermissions, CommandOnCooldown

class Lock(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  # Events
  @commands.Cog.listener()
  async def on_ready(self):
    print(f"🟢  > Cog geladen: {__name__}")

  # Commands
  @slash_command(name="lock", description="Sperre einen Textkanal")
  @commands.has_permissions(manage_channels=True)
  @commands.cooldown(1, 15, commands.BucketType.user)
  async def lock(self, ctx, channel: Option(discord.TextChannel, required=True, description="Wähle einen Kanal aus.")):
    await ctx.defer()

    logchannel = discord.utils.get(ctx.guild.channels, name="「📃」adminlog")

    overwrites = {
      ctx.guild.default_role: discord.PermissionOverwrite(send_messages=False)
    }

    await channel.edit(overwrites=overwrites)

    embed = discord.Embed(
      title=":lock: - Kanal gesperrt!",
      description=f"<#{channel.id}> wurde von **{ctx.author.name}** gesperrt.",
      color=discord.Color.red()
    )

    if not ctx.channel == channel:
      await ctx.respond(embed=embed)
      await channel.send(embed=embed)
    else:
      await ctx.respond(embed=embed)
    await logchannel.send(embed=embed)

  # Error
  @lock.error
  async def lock_error(self, ctx, error):
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
  bot.add_cog(Lock(bot))