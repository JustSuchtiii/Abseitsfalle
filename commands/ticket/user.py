import discord

from discord.ext import commands
from discord.commands import slash_command, Option
from discord.ext.commands.errors import MissingPermissions, BotMissingPermissions, CommandOnCooldown

class User(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  # Events
  @commands.Cog.listener()
  async def on_ready(self):
    print(f"🟢  > Cog geladen: {__name__}")


  # Commands
  ticket = discord.SlashCommandGroup("ticket-user", "Füge bzw. Entfernen einen User aus dem Ticket")  
  
  @ticket.command(name="add", description="Füge einen User zum Ticket hinzu")
  @commands.has_permissions(manage_channels=True)
  @commands.cooldown(1, 15, commands.BucketType.user)
  async def user_add(self, ctx, user: Option(discord.Member)):
    await ctx.defer()

    logchannel = discord.utils.get(ctx.guild.channels, name="「📃」adminlog")

    user_id = ctx.user.id
    guild = ctx.guild
    role = discord.utils.get(guild.roles, name="「🔧」Team")
    
    overwrites = {
      guild.default_role: discord.PermissionOverwrite(view_channel=False),
      user: discord.PermissionOverwrite(view_channel=True, send_messages=True),
      role: discord.PermissionOverwrite(view_channel=True)
    }

    embed = discord.Embed(
      title=":ticket: - Neuer User hinzugefügt!",
      description=f"**{user.name}** wurde zum Ticket (<#{ctx.channel.id}>) hinzugefügt.",
      color=discord.Color.yellow()
    ).set_footer(
      text=ctx.channel.name
    )

    await ctx.channel.edit(overwrites=overwrites)
    await ctx.respond(user.mention, embed=embed)
    await logchannel.send(embed=embed)

  @ticket.command(name="remove", description="Entferne einen User zum Ticket hinzu")
  @commands.has_permissions(manage_channels=True)
  @commands.cooldown(1, 15, commands.BucketType.user)
  async def user_rem(self, ctx, user: Option(discord.Member)):
    await ctx.defer()

    logchannel = discord.utils.get(ctx.guild.channels, name="「📃」adminlog")

    user_id = ctx.user.id
    guild = ctx.guild
    role = discord.utils.get(guild.roles, name="「🔧」Team")
    
    overwrites = {
      guild.default_role: discord.PermissionOverwrite(view_channel=False),
      user: discord.PermissionOverwrite(view_channel=False, send_messages=False),
      role: discord.PermissionOverwrite(view_channel=True)
    }

    embed = discord.Embed(
      title=":ticket: - User Entfernt!",
      description=f"**{user.name}** wurde im Ticket (<#{ctx.channel.id}>) entfernt.",
      color=discord.Color.yellow()
    ).set_footer(
      text=ctx.channel.name
    )

    await ctx.channel.edit(overwrites=overwrites)
    await ctx.respond(user.mention, embed=embed)
    await logchannel.send(embed=embed)

  # Error
  @user_add.error
  async def add_error(self, ctx, error):
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
    
  @user_rem.error
  async def rem_error(self, ctx, error):
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
  bot.add_cog(User(bot))