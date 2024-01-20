import discord

from discord.ext import commands
from discord.ext.commands.errors import CommandOnCooldown
from discord.commands import slash_command
from discord.interactions import Interaction

class Transfer(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  # Events
  @commands.Cog.listener()
  async def on_ready(self):
    print(f"🟢  > Cog geladen: {__name__}")

  # Commands
  @slash_command(name="transfer", description="Gebe neue Transfers bekannt.")
  @commands.cooldown(1, 15, commands.BucketType.user)
  async def transfer(self, ctx):
    await ctx.defer()
    await ctx.respond("Wähle aus:", view=TransferView(), ephemeral=True)
    return
  
  # Error
  @transfer.error
  async def transfer_error(self, ctx, error):    
    if isinstance(error, CommandOnCooldown):
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
  bot.add_cog(Transfer(bot))

# Transfermodal
class TransferModalBuy(discord.ui.Modal):
  def __init__(self, *args, **kwargs):
    super().__init__(
      discord.ui.InputText(
        label="Spieler",
        placeholder="Max Mustermann"
      ),
      discord.ui.InputText(
        label="von",
        placeholder="FC Musterstadt"
      ),
      discord.ui.InputText(
        label="zu",
        placeholder="Musterdorfer SC"
      ),
      discord.ui.InputText(
        label="Summe",
        placeholder="10500000"
      ),
      discord.ui.InputText(
        label="Mögliche Boni",
        placeholder="0"
      ),
      *args,
      **kwargs
    )

  async def callback(self, interaction: Interaction):
    if int(self.children[3].value) != 0:
      if int(self.children[4].value) == 0:
        embed = discord.Embed(
          title="✅ HERE WE GO!",
          description=f"**{self.children[0].value}** wechselt für **{self.children[3].value} €** von **{self.children[1].value}** zu **{self.children[2].value}**.",
          color=discord.Color.brand_green()
        ).set_footer(
          text="Die Meldungen werden ihnen Präsentiert von DCSlin."
        )
        msg = await interaction.response.send_message(embed=embed)
        return
      else:
        x = int(self.children[3].value) + int(self.children[4].value)
        embed = discord.Embed(
          title="✅ HERE WE GO!",
          description=f"**{self.children[0].value}** wechselt für **{self.children[3].value} €** von **{self.children[1].value}** zu **{self.children[2].value}**.\n\nMit möglichen Bonuszahlungen kann sich die Transfersumme auf **{x} €** erhöhen.",
          color=discord.Color.brand_green()
        ).set_footer(
          text="Die Meldungen werden ihnen Präsentiert von DCSlin."
        )
        msg = await interaction.response.send_message(embed=embed)
        return
    else:
      embed = discord.Embed(
        title="✅ HERE WE GO!",
        description=f"**{self.children[0].value}** wechselt **Ablösefrei** von **{self.children[1].value}** zu **{self.children[2].value}**.",
        color=discord.Color.brand_green()
      ).set_footer(
        text="Die Meldungen werden ihnen Präsentiert von DCSlin."
      )
      msg = await interaction.response.send_message(embed=embed)
      return
    
# Leihmodal
class TransferModalLoan(discord.ui.Modal):
  def __init__(self, *args, **kwargs):
    super().__init__(
      discord.ui.InputText(
        label="Spieler",
        placeholder="Max Mustermann"
      ),
      discord.ui.InputText(
        label="von",
        placeholder="FC Musterstadt"
      ),
      discord.ui.InputText(
        label="zu",
        placeholder="Musterdorfer SC"
      ),
      discord.ui.InputText(
        label="Leihgebür",
        placeholder="4000000"
      ),
      discord.ui.InputText(
        label="Mögliche Kaufoption",
        placeholder="0"
      ),
      *args,
      **kwargs
    )

  async def callback(self, interaction: Interaction):
    if int(self.children[4].value) == 0:
      embed = discord.Embed(
        title="☑️ HERE WE GO!",
        description=f"**{self.children[0].value}** wird für **{self.children[3].value} €** von **{self.children[1].value}** zu **{self.children[2].value}** verliehen.",
        color=discord.Color.brand_green()
      ).set_footer(
        text="Die Meldungen werden ihnen Präsentiert von DCSlin."
      )
      msg = await interaction.response.send_message(embed=embed)
      return
    else:
      embed = discord.Embed(
        title="☑️ HERE WE GO!",
        description=f"**{self.children[0].value}** wird für **{self.children[3].value} €** von **{self.children[1].value}** zu **{self.children[2].value}** verliehen.\n\nKaufoption: **{self.children[4].value} €**",
        color=discord.Color.brand_green()
      ).set_footer(
        text="Die Meldungen werden ihnen Präsentiert von DCSlin."
      )
      msg = await interaction.response.send_message(embed=embed)
      return

# View
class TransferView(discord.ui.View):
  @discord.ui.button(label="Transfer", style=discord.ButtonStyle.green)
  async def button_callback0(self, button, interaction):
    await interaction.response.send_modal(TransferModalBuy(title="Erstelle eine Bestätigung zu einem Transfer"))

  @discord.ui.button(label="Leihe", style=discord.ButtonStyle.green)
  async def button_callback1(self, button, interaction):
    await interaction.response.send_modal(TransferModalLoan(title="Erstelle eine Bestätigung zu einer Leihe"))