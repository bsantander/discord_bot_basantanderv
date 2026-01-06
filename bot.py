import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from utils.messages import load_messages, get_message

load_dotenv()

class MyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True # NECESARIO para leer el contenido de los mensajes de comandos con prefijo (ej: !hola)
        intents.members = True         # Si necesitas interactuar con miembros (ej: dar roles, o usar ciertos permisos)
        
        load_messages()
        
        super().__init__(
            command_prefix='!', 
            intents=intents,
            help_command=None
        )

    #carga de modulos, configuraciones -> solo se ejecuta al iniciar el bot
    async def setup_hook(self): 

        MY_GUILD = discord.Object(id=os.getenv("DISCORD_SERVER_TEST")) 

        #carga de cogs
        for ext in os.listdir("./cogs"):
            if ext.endswith(".py") and not ext.startswith("__"):
                try:
                    await self.load_extension(f"cogs.{ext[:-3]}")
                    msg = get_message(
                    "INICIALIZACION",
                    "COG_CARGADO",
                    cogs = ext
                    )
                except commands.ExtensionNotFound:
                    msg = get_message(
                        "INICIALIZACION",
                        "COG_NO_EXISTE",
                        cogs = ext
                    )  
                except commands.ExtensionError:
                    msg = get_message(
                        "INICIALIZACION",
                        "COG_CON_ERROR",
                        cogs = ext
                    )  
                print(msg)

        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)


    async def on_ready(self):
        """Se ejecuta cuando el bot se conecta a Discord."""
        msg = get_message(
            "INICIALIZACION",
            "ON_READY",
            bot_name = self.user.name
        )
        print(msg)







if __name__ == "__main__":
    bot = MyBot()
    TOKEN = os.getenv("DISCORD_TOKEN")

    if TOKEN:
        bot.run(TOKEN)
    else:
        print("Error: No se encontró el token de Discord en el archivo .env")