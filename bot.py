import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from utils.messages import load_messages, get_message

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True # NECESARIO para leer el contenido de los mensajes de comandos con prefijo (ej: !hola)
intents.members = True         # Si necesitas interactuar con miembros (ej: dar roles, o usar ciertos permisos)

bot = commands.Bot(command_prefix='/', intents=intents)

load_messages()

# CARGA DE COGS

async def load_cogs():
    """Carga los cogs del servidor y luego lanza un mensaje de exito/fallo"""
    try: #Carga de cog SERVIDOR
        cog = "servidor"
        await bot.load_extension('cogs.servidor')
        mensaje = get_message(
            "INICIALIZACION",
            "COG_CARGADO",
            cogs = cog
        )
        print(mensaje)
    except commands.ExtensionNotFound:
        mensaje = get_message(
            "INICIALIZACION",
            "COG_NO_EXISTE",
            cogs = cog
        )  
        print(mensaje)
    except commands.ExtensionError:
        mensaje = get_message(
            "INICIALIZACION",
            "COG_CON_ERROR",
            cogs = cog
        )  

    try: #Carga de cog MINECRAFT
        cog = "minecraft"
        await bot.load_extension('cogs.minecraft')
        mensaje = get_message(
            "INICIALIZACION",
            "COG_CARGADO",
            cogs = cog
        )
        print(mensaje)
    except commands.ExtensionNotFound:
        mensaje = get_message(
            "INICIALIZACION",
            "COG_NO_EXISTE",
            cogs = cog
        )  
        print(mensaje)
    except commands.ExtensionError:
        mensaje = get_message(
            "INICIALIZACION",
            "COG_CON_ERROR",
            cogs = cog
        )


# EVENTOS

@bot.event
async def on_ready():
    """Se ejecuta cuando el bot se conecta a Discord."""
    mensaje = get_message(
        "INICIALIZACION",
        "ON_READY",
        bot_name = bot.user.name
    )
    print(mensaje)
    await load_cogs()
    await bot.change_presence(activity=discord.Game(name="Escribiendo !help"))

# COMANDOS DE SERVIDOR

@bot.command(name='hola', help='El bot saluda.')
async def hola(ctx):
    """Comando simple que saluda al usuario."""
    mensaje = get_message(
        "COMANDOS",
        "HOLA_RESPUESTA",
        usuario = ctx.author.display_name
    )
    await ctx.send(mensaje)

@bot.command(name='info', help='Proporciona información sobre el bot.')
async def info(ctx):
    """Proporciona información básica sobre el bot."""
    embed = discord.Embed(title="Información del Bot", color=discord.Color.blue())
    embed.add_field(name="Nombre", value=bot.user.name, inline=False)
    embed.add_field(name="ID", value=bot.user.id, inline=False)
    embed.add_field(name="Desarrollador", value="Baztrock", inline=False)
    embed.set_footer("Bot de uso interno para servidores de Baztrock.")
    await ctx.send(embed=embed)

@bot.command(name='ping', help='Responde con Pong y la latencia del bot.')
async def ping(ctx):
    """Responde con la latencia del bot."""
    latency = bot.latency
    mensaje = get_message(
        "COMANDOS",
        "PING",
        ping = latency
    )
    await ctx.send(mensaje)


@bot.command(name='encender', help='Encender el Servidor y panel')
async def encender(ctx):
    """Tareas automatizadas para inicio de servidor donde esta el nodo principal"""

    servidor = bot.get_cog("ServidorCog")
    if servidor:
        inicio = servidor.iniciar_servidor()
    await ctx.send('Encendiendo panel y servidor...')
    if inicio:
        mensaje = get_message(
            "COMANDOS",
            "SERVER_INICIADO"
        )
        await ctx.send(mensaje)
    else:
        mensaje = get_message(
            "COMANDOS",
            "SERVER_NO_INICIADO"
        )

@bot.command(name='estado', help='Comprueba el estado del servidor, si este esta encendido o apagado')
async def estado(ctx):
    """Entrega mensaje de estado de servidor, si este esta encendido o no"""
    estadoServidor = bot.get_cog("ServidorCog")


# comando con manejo de permisos como ejemplo de uso
@bot.command(name='limpiar', help='Elimina una cantidad específica de mensajes. (Requiere el permiso "Manage Messages").')
@commands.has_permissions(manage_messages=True)
async def limpiar(ctx, cantidad: int):
    """
    Elimina 'cantidad' de mensajes en el canal donde fue llamado.
    El decorador @commands.has_permissions(manage_messages=True) se encarga de la verificación.
    """
    if cantidad <= 0:
        await ctx.send("Por favor, introduce un número positivo de mensajes a eliminar.")
        return

    deleted = await ctx.channel.purge(limit=cantidad + 1) 
    
    # Envía una confirmación y la borra después de 5 segundos
    await ctx.send(f'Se eliminaron {len(deleted) - 1} mensajes.', delete_after=5)

# --- MANEJO DE ERRORES DE PERMISOS ---

@bot.event
async def on_command_error(ctx, error):
    """Maneja errores específicos de comandos, como la falta de permisos."""
    if isinstance(error, commands.MissingPermissions):
        mensaje = get_message(
            "ERRORES",
            "FALTA_PERMISO",
            usuario = ctx.author.display_name,
            permiso = ", ".join(error.missing_permissions)
        )
        await ctx.send(
            mensaje,
            delete_after=10
        )
    else:
        print(f'Ocurrió un error: {error}')
        await ctx.send('Ocurrió un error inesperado. Por favor, revisa la consola.')


# 4. Iniciar el Bot
if TOKEN:
    bot.run(TOKEN)
else:
    print("Error: No se encontró el token de Discord en el archivo .env.")