

import sys
import socket
import select
import redis


# Ejemplo de uso:
#   python3 ejercicio1_cliente_redis.py <nick> <ip_redis>
#
# Donde:
#   <nick>      → nombre de usuario en el chat
#   <ip_redis>  → dirección IP del servidor Redis
#
if len(sys.argv) != 3:
    print("Uso: python3 ejercicio1_cliente_redis.py <nick> <ip_redis>")
    sys.exit(1)

nick = sys.argv[1]
ip_redis = sys.argv[2]
puerto_chat = 5000  # Puerto UDP en el que el cliente escucha mensajes


# Conectamos con el servidor Redis (por defecto, puerto 6379)
redis_client = redis.Redis(host=ip_redis, port=6379, db=0)

# Comprobamos si el nombre ya existe para evitar duplicados
if redis_client.exists(nick):
    print(f"El nombre '{nick}' ya está en uso.")
    sys.exit(1)

# Registramos nuestro nick con la IP local y el puerto UDP
ip_local = socket.gethostbyname(socket.gethostname())
redis_client.set(nick, f"{ip_local}:{puerto_chat}")
print(f"Registrado en Redis como {nick} ({ip_local}:{puerto_chat})")


# Se usa para enviar y recibir mensajes entre clientes
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("", puerto_chat))  # Escucha en todas las interfaces disponibles

# Variables para guardar la dirección del destinatario actual
ip_destino = None
puerto_destino = None

print("\nComandos:")
print("/CHAT <nick_destino>  → Iniciar chat con otro usuario")
print("/QUIT                 → Salir del programa\n")

while True:
    # select() permite esperar simultáneamente por entrada de teclado o mensajes UDP
    lista_lectura, _, _ = select.select([sys.stdin, s], [], [])

    # Si se recibe un mensaje por UDP, se muestra en pantalla
    if s in lista_lectura:
        datos, _ = s.recvfrom(1024)
        print("\n" + datos.decode())

    # Si el usuario escribió algo en la terminal
    if sys.stdin in lista_lectura:
        mensaje = sys.stdin.readline().strip()

        # Comando para salir
        if mensaje.upper() == "/QUIT":
            print("Cerrando sesión...")
            redis_client.delete(nick)  # Eliminamos nuestro registro de Redis
            s.close()
            break

        # Comando para iniciar chat con otro usuario
        elif mensaje.upper().startswith("/CHAT"):
            partes = mensaje.split()
            if len(partes) != 2:
                print("Uso: /CHAT <nick_destino>")
                continue

            nick_destino = partes[1]

            # Consultamos Redis para obtener la dirección del destino
            valor = redis_client.get(nick_destino)
            if valor is None:
                print("El usuario no está conectado.")
                continue

            ip_destino, puerto_destino = valor.decode().split(":")
            puerto_destino = int(puerto_destino)
            print(f"Ahora estás chateando con {nick_destino} ({ip_destino}:{puerto_destino})")

        # Si hay chat activo, enviamos mensaje al destinatario
        elif ip_destino and puerto_destino:
            texto = f"{nick}: {mensaje}"
            s.sendto(texto.encode(), (ip_destino, puerto_destino))

        # Si no hay chat activo, recordamos el comando necesario
        else:
            print("No hay chat activo. Usa /CHAT <nick_destino> para iniciar uno.")

