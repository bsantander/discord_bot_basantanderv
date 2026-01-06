import discord
from discord import app_commands
from discord.ext import commands
from utils.messages import get_message
import utils.node_server as ns

class ServidorCog(commands.Cog):
    
    # Funcion de carga del cog

    def __init__(self, bot):
        self.bot = bot        

    @app_commands.command(name="encender", description="Encender nodo servidor.")
    async def encendido_nodo(self, interaction: discord.Interaction):
        
        msg = get_message(
            "COMANDOS",
            "ENCENDIENDO_NODO"
        )
        await interaction.response.send_message(msg)
        
        estado = await ns.iniciar_servidor()

        if estado == "SUCCESS":
            msg = get_message(
                "COMANDOS",
                "SERVER_INICIADO"
            )
        elif estado == "SERVER_ON":
            msg = get_message(
                "COMANDOS",
                "SERVER_ON"

            )
        else:
            msg = get_message(
                "ERRORES",
                "SERVER_NO_INICIADO"

            )

        await interaction.edit_original_response(content=msg)

    @app_commands.command(name="apagar", description="Apagar el nodo servidor.")
    async def apagado_nodo(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        resultado = await ns.comando_a_nodo("sudo /usr/sbin/shutdown now")   
        
        await interaction.edit_original_response(content=f"**Resultado:**\n```bash\n{resultado}```")

    
async def setup(bot):
    await bot.add_cog(ServidorCog(bot))