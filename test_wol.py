from wakeonlan import send_magic_packet
import os
from dotenv import load_dotenv


load_dotenv()

mac = os.getenv("NODE_MAC") # Formato '00:11:22:33:44:55'
# Intenta con la IP de broadcast universal si no sabes la de tu red
broadcast = '192.168.1.255' 

print(f"Enviando señal a {mac} vía {broadcast}...")
try:
    send_magic_packet(mac, ip_address=broadcast)
    print("✅ Paquete enviado. Si no enciende, revisa el broadcast o el puerto.")
except Exception as e:
    print(f"❌ Error: {e}")