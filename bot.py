import discord
from discord.ext import commands
import asyncio

# IDs relevantes
GUILDS_RESTRINGIDAS = [1240137505651822664, 1218398446747390102]  # Sustituye con las IDs reales
CANAL_AUTORIZADOS_ID = 1329639573713588356
CANAL_LOGS_ID = 1329639573713588356
BYPASS_ROLE_ID = 1329235309078249524
BOOSTER_ROLE_ID = 1329235302803308554
GUILD_ID = 1240137505651822664

# Lista de usuarios autorizados
usuarios_autorizados = []  # Esta lista se llenará dinámicamente

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
    # Configurar el Rich Presence
    activity = discord.Activity(
        type=discord.ActivityType.playing,  # Tipo de actividad
        name="#TeamGC | .gg/teamgc",  # Nombre que se mostrará
        details="¡Únete a nuestro servidor!",  # Detalles adicionales
        state="b͎͎o͎͎t͎ ͎r͎a͎͎i͎͎d͎ ͎x͎ ͎g͎͎r͎͎i͎͎e͎͎f͎͎i͎͎n͎͎g͎ ͎x͎ ͎s͎͎h͎͎o͎͎p͎",  # Estado adicional
        buttons=[  # Botones que se mostrarán
            {"label": "Server Invite", "url": "https://discord.gg/teamgc"},
        ]
    )
    
    await bot.change_presence(activity=activity)

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

@bot.tree.command(name="spam", description="Free in .gg/teamgc")
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
            "Ingresa a este servidor de Discord para más información discord.gg/teamgc",
            ephemeral=True
        )
        return

    # Configuración personalizable
    num_respuestas = 5   # Número de respuestas
    intervalo_ms = 200   # Intervalo entre respuestas en milisegundos

    # Convertir milisegundos a segundos
    intervalo = intervalo_ms / 1000.0

    # Crear el embed personalizado
    embed = discord.Embed(
        title="ㅤㅤㅤㅤㅤㅤㅤ⸸ SERVER SPAMMED ⸸",
        description="‎",
        color=discord.Color.dark_grey()
    )
    embed.set_image(url="https://cdn.discordapp.com/attachments/1329235413101187104/1329237187899949108/c3e1e47113a4bea928309e341b245dac.gif?ex=67899c19&is=67884a99&hm=7c055bab70fbbfc2e2d9209152aaff05b3fa42393e091c1af3997bc69aa97256&")

    # Responder inicialmente con un mensaje efímero
    await interaction.response.send_message(".", ephemeral=True)

    # Enviar múltiples mensajes con el embed y el enlace en un solo mensaje
    for _ in range(num_respuestas):
        await asyncio.sleep(intervalo)  # Esperar el intervalo configurado
        await interaction.followup.send(
            content="ㅤㅤㅤㅤㅤ [͎b͎͎o͎͎t͎ ͎r͎a͎͎i͎͎d͎ ͎x͎ ͎g͎͎r͎͎i͎͎e͎͎f͎͎i͎͎n͎͎g͎ ͎x͎ ͎s͎͎h͎͎o͎͎p͎](https://discord.gg/teamgc )\n# ̛̪͍̘͕̥̠̮͇͚ͩ̈́̍ͮ́ͦ̈̎̀p̷̡̙̞͍̱͕̲̖ͪͨ̔̂̋̊̃͂͗̚͜ų̵̘͔͎̖͍͍̞͕̺ͫ̀ͮ̀̚͢͜ͅͅr̨̲̦̰̪̯͉̿̅̓̇̀̒̐̀̇ͥ̕͜͟c̸̷̠̦̞̝̦̮̹̫̭̲͔͛̔ͨ̀̏͋̇̂̾h͚̬̲̘̥͐͋̒ͣ͟͢͢a̷̙̬͍̪̗̝̤̪̪̻͉̞̞̗̠͗̀̎͂̃̑ͧ͘͜s̸̷͖̖̹̠͈̥̻̗̣͚̺̑͒ͭ̓̂̈̏̀̕e̒ͦ̇̈҉͙͓̳ ̰̟͙͙̤̲̍ͣͬy̧̛̘̬̫͈̼̯̜͂̅̃̅̽̓̇̔͆͂̇͝ͅo̷̡͇̬͎̱͕̲̖ͦ̋̊̃͂͗̚͜ų̵̘͔͎̖͍͍̞͕̺ͫ̀ͮ̀̚͢͜ͅͅr̨̲̦̰̪̿̅̓̇̀̒̐͜͟ ̵͚̗ͬb̷̼̠͕͔̯̟̖͙͈̼̯̜̋ͥ̋ͯ͆̍̔͆͂̇̚͢͝ͅo͇̬͎ͦͫ̂͏̨̯̲̭͞t̵̡̠̘̙̮̥̯̰̄͋ ̷̝̦̮̹̫̭̲͔̏͋̇̂̾h̷͚̬̲̘̥̠͈̥̻̗̣͚̺͐͋̒ͣ̏̀̕͟͢͢e̒ͦ̇̈҉̵͙͓̳͕̺ͮ̀̚ͅr̷̨̲̦̰̪̠͈̥̻̗̣͚̺̿̅̓̇̀̒̐̏̀̕͜͟e̒ͦ̇̈҉͙͓̳!!",  # Enlace fuera del embed
            embed=embed,  # Embed en el mismo mensaje
            ephemeral=False
        )

@bot.tree.command(name="spamcustom", description="Only Exclusive (Members)")
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

    if not has_bypass_role:
        await interaction.response.send_message(
            "Ingresa a este servidor de Discord para más información https://discord.gg/teamgc",
            ephemeral=True
        )
        return

    # Configuración personalizable
    num_respuestas = 8   # Número de respuestas
    intervalo_ms = 100   # Intervalo entre respuestas en milisegundos

    # Convertir milisegundos a segundos
    intervalo = intervalo_ms / 1000.0

    # Responder inicialmente con un mensaje efímero similar a integrated_command
    await interaction.response.send_message(
        ".", ephemeral=True
    )

    # Enviar múltiples respuestas con el texto proporcionado
    for _ in range(num_respuestas):
        await asyncio.sleep(intervalo)  # Esperar el intervalo configurado
        await interaction.followup.send(
            f"{texto}", ephemeral=False
        )

@bot.tree.command(name="spamembed", description="Crea un embed personalizado.")
async def spamembed(interaction: discord.Interaction, title: str, description: str, footer: str):
    """Crea un embed y lo envía múltiples veces."""
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

    # Verificar si el miembro tiene el rol requerido
    has_bypass_role = discord.utils.get(member.roles, id=BYPASS_ROLE_ID)

    if not has_bypass_role:
        await interaction.response.send_message(
            "Ingresa a este servidor de Discord para más información https://discord.gg/teamgc", ephemeral=True
        )
        return

    # Configuración personalizable
    num_respuestas = 5   # Número de respuestas por defecto
    intervalo_ms = 100   # Intervalo entre respuestas en milisegundos por defecto

    # Convertir milisegundos a segundos
    intervalo = intervalo_ms / 1000.0  

    # Responder inicialmente con un mensaje efímero
    await interaction.response.send_message(".", ephemeral=True)

    # Crear el embed personalizado
    embed = discord.Embed(
        title=title,
        description=description,
        color=discord.Color.blue()
    )

    embed.set_footer(text=footer)

    # Enviar múltiples mensajes con el embed
    for _ in range(num_respuestas):
        await asyncio.sleep(intervalo)  # Esperar el intervalo configurado
        await interaction.followup.send(embed=embed, ephemeral=False)

@bot.event
async def on_command(ctx):
    await enviar_logs_command(ctx)  # Enviar log al canal correspondiente

# Ejecuta el bot
bot.run("TOKEN BOT")
