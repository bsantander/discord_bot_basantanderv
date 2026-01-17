import os
import time
import socket
import asyncio
import asyncssh
import wakeonlan
from utils.messages import get_message

def _ping_to_server(ip=os.getenv("NODE_IP"), puerto = 22):
    """Servicio de ping to server, como default value se usa la ip del nodo servidor y el puerto 22

    Args:
        ip (_type_, optional): _description_. Defaults to os.getenv("NODE_IP").
        puerto (int, optional): _description_. Defaults to 22.

    Returns:
        bool: _description_. si el servidor acepta conexiones
        float: _description_. ping en ms
    """

    inicio = time.perf_counter()
    
    try:
        with socket.create_connection((ip, puerto), timeout=1):
            fin = time.perf_counter()
            latencia_ms = round((fin - inicio) * 1000)
            return True, latencia_ms
    except (OSError, socket.timeout):
        return False, None
    
async def comprobar_encendido_servidor():
    ip = os.getenv('NODE_IP')
    if not ip:
        print(get_message("DEPURACION", "FALTA_VARIABLE", variable="NODE_IP"))
        return False
    online, ms = await asyncio.to_thread(_ping_to_server, ip)
    return online

async def iniciar_servidor():
    if await comprobar_encendido_servidor():
        return "SERVER_ON"
    
    mac = os.getenv("NODE_MAC")
    print(mac)
    if not mac:
        mensaje = get_message(
            "DEPURACION",
            "FALTA_VARIABLE",
            variable = "NODE_MAC"
        )
        print(mensaje)
        return "ERR_NOT_MAC"
    print(get_message(
        "DEPURACION",
        "ENVIAR_M_PACKET"
    ))    
    wakeonlan.send_magic_packet(mac, ip_address="192.168.1.255")
    print(get_message(
        "DEPURACION",
        "ENVIADO_M_PACKET"
    ))


    for i in range(6):
        await asyncio.sleep(5)
        if await comprobar_encendido_servidor():
            return "SUCCESS"
    return "FAILED"

async def comando_a_nodo(comando, hostname=None, user=None, key_path=None):
    
    hostname=os.getenv("NODE_IP") 
    user=os.getenv("NODE_SSH_USER") 
    key_path=os.getenv("NODE_SSH_KEY_PATH")
    
    print(f"DEBUG: Host={hostname}, User={user}, Key={key_path}")
    try:
        async with asyncssh.connect(host=hostname, username=user, client_keys=[key_path], known_hosts= None) as connection:
            resultado = await connection.run(comando, check=True)
            return resultado.stdout.strip()

    except(asyncssh.ProcessError) as exc:
        return f"Error de servidor: {exc.exit_status} -> {exc.stderr.strip()}"    
    except(OSError, asyncssh.Error) as exc:
        return f"Error de conexion: {exc}"