import asyncio
import os
import subprocess
from discord.ext import commands
import wakeonlan
from ..utils.messages import get_message

class ServidorCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot        

    async def _ping_to_server(self, ip_address):
        comando = ["ping", "-c 1", ip_address]

        try:
            resultado = subprocess.run(
                comando,
                capture_output=True,
                check=False,
                text=True
            )
            return resultado.returncode == 0
        
        except FileNotFoundError:
            mensaje = get_message(
                "DEPURACION",
                "FALTA_COMANDO",
                comando = "ping"
            )
            print(mensaje)
            return False

    async def comprobar_encendido_servidor(self):
        ip = os.getenv('SERVER_IP')
        if not ip:
            mensaje = get_message(
                "DEPURACION",
                "FALTA_VARIABLE",
                variable = "SERVER_IP"
            )
            print(mensaje)
            return False
        
        esta_encendido = await asyncio.to_thread(self._ping_to_server, ip)
        return esta_encendido
    


    async def iniciar_servidor(self):
        if not await self.comprobar_encendido_servidor():
            mac = os.getenv('SERVER_MAC')
            if mac:
                wakeonlan.send_magic_packet(mac)
                return 
            else:
                mensaje = get_message(
                    "DEPURACION",
                    "FALTA_VARIABLE",
                    variable = "SERVER_MAC"
                )
                print(mensaje)
        return 

async def setup(bot):
    await bot.add_cog(ServidorCog(bot))