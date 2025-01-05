import discord
from discord.ext import commands
import asyncio

# IDs relevantes
GUILDS_RESTRINGIDAS = [ID_GUILD1, ID_GUILD2]
CANAL_AUTORIZADOS_ID = 1320454163519246418 # Esto es donde llegaran los usuarios autorizados en el bot
CANAL_LOGS_ID = 123456789123456456 # Logs de los bots
BYPASS_ROLE_ID = 123456789123456456 # Role Bypass para el acceso a todos los comandos del bot
BOOSTER_ROLE_ID = 123456789123456456 # Role Bypass para el acceso de todos los comandos
GUILD_ID = 123456789123456456 # Guild ID Principal

usuarios_autorizados = []

class MyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.members = True  # Necesario para obtener la lista de miembros
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        await self.tree.sync()
        print("Comandos sincronizados.")

bot = MyBot()

@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")

async def enviar_logs_command(ctx):
    """Envia un log del comando ejecutado al canal de logs."""
    canal_logs = bot.get_channel(CANAL_LOGS_ID)
    if canal_logs:
        tag_name = f"{ctx.author.name}#{ctx.author.discriminator}"
        server_name = ctx.guild.name if ctx.guild else "Mensaje Directo"
        await canal_logs.send(f"- **Tag Name**: {tag_name}\n- **Server Name**: {server_name}")

async def actualizar_embed_autorizados():
    """Actualiza el embed en el canal de miembros autorizados."""
    canal_autorizados = bot.get_channel(CANAL_AUTORIZADOS_ID)
    if not canal_autorizados:
        print("No se encontró el canal de miembros autorizados.")
        return

    # Crear el embed con la lista de usuarios autorizados
    embed = discord.Embed(
        title="Members Authorized's",
        color=discord.Color.blue()
    )
    if usuarios_autorizados:
        for user in usuarios_autorizados:
            embed.add_field(name="\u200b", value=f"{user.mention}", inline=False)
    else:
        embed.description = "No hay usuarios autorizados aún."

    # Buscar el último mensaje en el canal y editarlo si es del bot
    async for message in canal_autorizados.history(limit=10):
        if message.author == bot.user:
            await message.edit(embed=embed)
            return

    # Si no hay mensajes del bot, envía uno nuevo
    await canal_autorizados.send(embed=embed)

@bot.tree.command(name="spam", description="Only Boosters and VIP")
async def integrated_command(interaction: discord.Interaction):
    guild = bot.get_guild(GUILD_ID)

    if not guild:
        await interaction.response.send_message(
            "No se pudo encontrar la guild especificada.", ephemeral=True
        )
        return

    member = guild.get_member(interaction.user.id)
    if not member:
        await interaction.response.send_message(
            "No se pudo encontrar al miembro en la guild especificada.", ephemeral=True
        )
        return

    # Verificar si el miembro tiene los roles requeridos
    has_bypass_role = discord.utils.get(member.roles, id=BYPASS_ROLE_ID)
    has_booster_role = discord.utils.get(member.roles, id=BOOSTER_ROLE_ID)

    if not has_bypass_role and not has_booster_role:
        await interaction.response.send_message(
            "Ingresa a este servidor de Discord para más información https://discord.gg/mYwaxNAkZ6",
            ephemeral=True
        )
        return

    # Respuesta si tiene los roles requeridos
    # Configuración personalizable
    num_respuestas = 5   # Número de respuestas
    intervalo_ms = 200   # Intervalo entre respuestas en milisegundos

    # Convertir milisegundos a segundos
    intervalo = intervalo_ms / 200.0

    # Crear el embed personalizado
    embed = discord.Embed(
        title="⸸                SERVER SPAMMED POR ONUSQUAD                ⸸",
        description="S̴͖͍͙͗̂͊̏̽̀̔́̓͆̉̽͘͝ë̵̡̳̯̙̖̣͓̩́̆̐̀̾̈́͊̾̈́̈́̎̈́͘͝ͅr̷̨̢̥͈͕̪̞̦̼͔̞͚̓̽́͋̂̃͆̚͜v̴͕̓͆̇̆̈́͗̍́̍̏͐̾̀̇̒ė̶̮̓̈́̋̑̑̋́̐̓̀ŕ̷̢̐̐́̓̔̊̓̊́́̈́̚͝ ̶̢͈̯̫̥͚̠̘̍Ŝ̷̼͓̦͉̜̦̫͌͌̃̃͗́͒͋̓́̐͘̕͝ͅp̶̭͓̤̰̭͊̿̾̇̌͝ȧ̸̝̭̅̉͝m̸̢̢̬͇̮͕͎͎̲̪̊͒̀̈́͐̈ͅm̴̢̢̟̗̫͍͔͙̖̹͋̀̂̈́͒̂̈́͗̍̀̏͜ͅe̵̢̛̙̭̺̜̬͖͙̺̭͆͒͒̊̉̋̐̍̓̑͜ͅͅd̸̫̝̮̞̜̱͓̥̥̈̉̓̒͘͠ ̴̨͈̘̟͇͎̰̘̾͆̈̀͛̓̚͝b̷̨̹̰̱͇̲͖̝̝͇̓̽͂͐̍̍́͌̓̽͊̍͝͝y̵̺̫̞̜̘̆̏̓̀̍̊̋͋̈͘ ̵̗̭͉̖͉͆̿̈́́̀̂̉̕͠͝͠Ǫ̷̯̦̠͉̒͑͛n̸̙͍̗̟͚̮͕͙̊́͌̊́̏͆̏̉̐̌̚͝͝ͅȕ̵̢͚̰̞̪̥̹̊͑͒̊̓͑͊̿͂͗S̴̰̒̎͒̉̈̌͊̚͝q̴̧̰̻̤͙͗͆͑͛̄̍͒̃͐u̶̗̜͗̽͌͐̕̚͠ͅá̴͇̺͖͖̤́̀̍̾̏͘ͅḑ̵̔̄̑ ̴̨̧͕̗̝̼͕͇̣̣͉̮͆̽̃̿̿̅̉̆͌̎̿̚͘b̶͖̥̮̄͆̆̈́̄̑͘ú̸̮̫̰̯̝́̓̾̋͒͋̍̑̽̅̕ͅy̶̢̜̹̰͎̫̗͍̪̣̞͙͚̒͠ͅ ̴̤̲̟̹̓́̽͝͝ŏ̸͍̜̙ͅŕ̵̬̱̔͐̄̈̾̌͆̊̕̕͝͝͠ ̴̥͐̇͗B̷͍̲̳͓͖͎̣͑̒͂̓̈́̓̓̆͌̄̔̊̈́͘͝ơ̷̢̨̫̣̤̪̭̤͎͕̦̖̬̜̅̒̑̌͆̌̑̏̆͊͌̍̄̚ó̶̤̾ș̸̢͇̺̹͈͊͜ṱ̷̼͉̥̳̅̑͠ȉ̷̖͎͇̲ͅņ̷͔̙̑̈́̀̄̆̑̾̕͝ģ̷̻̳̰͚̰̜̲̀̏͊̂̽̊ͅ ̶̩̰͎̥̳̱̤̦͓̺̃̂̅ḟ̸̡̯̤͙̳̫̣̪̟̓͑͊͛̇͘͠o̷̱̖͉̓ŗ̶̼̰̗̺͛͒̋̏͘ ̵͙̥̃̾̎́͋͛͛͛͘͝͝Ş̵̛̛̘̘̦̦̋͐͑̽͊̔͂͂̽̔͂̕͘͜ṗ̸̨͎͓̝͕̥̹̻̥ą̶̛͙͉͖̪̟̮̻͇̼͚̗̅͛̽̏͜͝m̷̠̠̻̟̮̝̟͈̺͍͇̃̍̊̚ ̸̘̘̳̤̦̝̗̺̼̫̖͆̈́͊́̆̀͒̌͛̒̏̓̕̚͝B̶̢͈̺̤͉̭̼͚̺̈͗̔̂̃̋̅̀́̀͗̆̇͆ǒ̷̺̲̣̺̳̩̭̫̘̓̈͘ͅt̷̨̰̞̖̰̤̼̺̦̥͉͒͛́̇͑̂̋͆ͅͅ",
        color=discord.Color.dark_grey()
    )
    embed.add_field(name="\u200b", value="‎ ‎‎ ‎‎ ‎‎ ‎ ‎‎ ‎‎ ‎‎ ‎ ‎‎ ‎‎ ‎‎ ‎ ‎‎ ‎‎ ‎‎ ‎ ‎‎ ‎‎ ‎‎ ‎ ‎‎ ‎‎ ‎‎ ─────────✦─────────‎ ‎‎ ‎‎ ‎‎ ‎ ‎‎ ‎‎ ‎‎ ", inline=False)  # Separador decorativo
    embed.set_footer(text="#OnuSquad")
    embed.set_image(url="https://cdn.discordapp.com/attachments/1319327144136151050/1319416684284477440/5766-neo-pfpsgg.gif?ex=676a7f4b&is=67692dcb&hm=eaf127ab02d03aef89c327dce3eb7f0db294010604dc74e0f9e6d7b982cfcb3a&")  # Cambia esto por la URL de tu imagen.

    # Responder inicialmente con un mensaje efímero
    await interaction.response.send_message(".", ephemeral=True)

    # Enviar múltiples mensajes con el embed y el enlace en un solo mensaje
    for _ in range(num_respuestas):
        await asyncio.sleep(intervalo)  # Esperar el intervalo configurado
        await interaction.followup.send(
            content="# https://discord.gg/mYwaxNAkZ6",  # Enlace fuera del embed
            embed=embed,  # Embed en el mismo mensaje
            ephemeral=False
        )

@bot.tree.command(name="spamcustom", description="Only Boosters and VIP")
async def testcustom(interaction: discord.Interaction, texto: str):
    """Recibe texto del usuario y responde con ese mismo texto."""
    guild = bot.get_guild(GUILD_ID)

    if not guild:
        await interaction.response.send_message(
            "No se pudo encontrar la guild especificada.", ephemeral=True
        )
        return

    member = guild.get_member(interaction.user.id)
    if not member:
        await interaction.response.send_message(
            "No se pudo encontrar al miembro en la guild especificada.", ephemeral=True
        )
        return

    # Verificar si el miembro tiene los roles requeridos
    has_bypass_role = discord.utils.get(member.roles, id=BYPASS_ROLE_ID)
    has_booster_role = discord.utils.get(member.roles, id=BOOSTER_ROLE_ID)

    if not has_bypass_role and not has_booster_role:
        await interaction.response.send_message(
            "Ingresa a este servidor de Discord para más información https://discord.gg/mYwaxNAkZ6",
            ephemeral=True
        )
        return

    # Configuración personalizable
    num_respuestas = 5   # Número de respuestas
    intervalo_ms = 200   # Intervalo entre respuestas en milisegundos

    # Convertir milisegundos a segundos
    intervalo = intervalo_ms / 200.0

    # Responder inicialmente con un mensaje efímero similar a integrated_command
    await interaction.response.send_message(
        ".", ephemeral=True
    )

    # Enviar múltiples respuestas con el texto proporcionado
    for _ in range(num_respuestas):
        await asyncio.sleep(intervalo)
        await interaction.followup.send(
            f"{texto}", ephemeral=False
        )

@bot.event
async def on_command(ctx):
    await enviar_logs_command(ctx)

bot.run("TOKEN")
