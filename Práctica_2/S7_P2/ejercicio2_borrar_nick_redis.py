import sys
import redis
import socket

def obtener_ip_local():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))
    ip_local = s.getsockname()[0]
    s.close()
    return ip_local

# Comprobación de argumentos
if len(sys.argv) != 3:
    print(f"Uso: {sys.argv[0]} <ip_redis> <nick>")
    sys.exit(1)

ip_redis = sys.argv[1]
nick = sys.argv[2]

try:
    ip_local = obtener_ip_local()
    print(f"IP local detectada: {ip_local}")

    redis_client = redis.Redis(host=ip_redis, port=6379, db=0)
    resultado = redis_client.delete(nick)

    if resultado == 1:
        print(f"Clave '{nick}' eliminada correctamente de Redis.")
    else:
        print(f"No existe ninguna clave '{nick}' en Redis.")
except Exception as e:
    print(f"Error al conectar o eliminar la clave: {e}")
    sys.exit(1)
