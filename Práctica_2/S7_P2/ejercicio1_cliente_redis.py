
"""
Uso:
    python3 ejercicio1_cliente_redis.py <nick> <ip_redis>
"""

import sys
import socket
import select
import redis


# Comprobación de argumentos 
if len(sys.argv) != 3:
    print("Uso: python3 ejercicio1_cliente_redis.py <nick> <ip_redis>")
    sys.exit(1)

nick = sys.argv[1]        # Nombre de usuario en el chat
ip_redis = sys.argv[2]    # Dirección IP del servidor Redis


#  Función auxiliar para obtener IP local
def obtener_ip_local():

    ip = "127.0.0.1"
    tmp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        tmp.connect(("8.8.8.8", 80))   # dirección arbitraria
        ip = tmp.getsockname()[0]
    except Exception:
        pass
    finally:
        tmp.close()
    return ip


#  Conexión con Redis 
try:
    # decode_responses=True → las respuestas vienen como str (no bytes)
    redis_client = redis.Redis(host=ip_redis, port=6379, db=0, decode_responses=True)
    redis_client.ping()  # Comprobamos conexión
except Exception as e:
    print(f"No se pudo conectar a Redis en {ip_redis}:6379 -> {e}")
    sys.exit(1)


# Registro del cliente en Redis 
ip_local = obtener_ip_local()

# Creamos el socket UDP (0 = que el SO elija un puerto libre)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("", 0))
puerto_chat = s.getsockname()[1]

# Comprobamos si el nick ya está en uso
if redis_client.exists(nick):
    print(f"El nombre '{nick}' ya está en uso.")
    s.close()
    sys.exit(1)

# Registramos nuestro nick con IP:puerto en Redis
try:
    redis_client.set(nick, f"{ip_local}:{puerto_chat}")
    print(f"Registrado en Redis como {nick} ({ip_local}:{puerto_chat})")
except Exception as e:
    print(f"No se pudo registrar el nick en Redis: {e}")
    s.close()
    sys.exit(1)


# Interfaz de usuario
print("\nComandos disponibles:")
print("/CHAT <nick_destino>  → Iniciar chat con otro usuario")
print("/QUIT                 → Salir del programa\n")

# Variables que almacenarán el destino del chat activo
ip_destino = None
puerto_destino = None


# Bucle principal 
while True:
    # select() espera simultáneamente entrada por teclado o mensajes UDP
    lista_lectura, _, _ = select.select([sys.stdin, s], [], [])

    # Si se recibe un mensaje UDP
    if s in lista_lectura:
        datos, _ = s.recvfrom(1024)
        print("\n" + datos.decode())   # Mostramos el mensaje recibido

    # Si el usuario escribió algo en la terminal
    if sys.stdin in lista_lectura:
        mensaje = sys.stdin.readline().strip()

        # Comando /QUIT
        if mensaje.upper() == "/QUIT":
            print("Cerrando sesión...")

            # Eliminamos nuestro registro de Redis
            try:
                redis_client.delete(nick)
            except Exception:
                pass

            s.close()
            break

        # Comando /CHAT <nick_destino>
        elif mensaje.upper().startswith("/CHAT"):
            partes = mensaje.split()
            if len(partes) != 2:
                print("Uso: /CHAT <nick_destino>")
                continue

            nick_destino = partes[1]

            # Consultamos Redis para obtener dirección del otro usuario
            valor = redis_client.get(nick_destino)
            if valor is None:
                print("El usuario no está conectado o no existe.")
                continue

            # Separamos IP y puerto
            ip_destino, puerto_destino = valor.split(":")
            puerto_destino = int(puerto_destino)

            print(f"Ahora estás chateando con {nick_destino} ({ip_destino}:{puerto_destino})")

        # Envío de mensaje normal
        elif ip_destino and puerto_destino:
            texto = f"{nick}: {mensaje}"
            try:
                s.sendto(texto.encode(), (ip_destino, puerto_destino))
            except Exception as e:
                print(f"Error enviando mensaje: {e}")

        # Si no hay chat activo
        else:
            print("No hay chat activo. Usa /CHAT <nick_destino> para iniciar uno.")

