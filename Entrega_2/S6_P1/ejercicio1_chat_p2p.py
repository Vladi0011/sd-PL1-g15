#!/usr/bin/env python3              # Indica al sistema que use Python 3 para ejecutar el archivo
# Chat P2P por UDP con select, sin funciones ni main()
# Uso desde la terminal: python3 chatear.py <puerto> <nick>

import sys                          # Módulo para acceder a argumentos y entrada estándar (teclado)
import socket                       # Módulo que permite usar conexiones de red (UDP/TCP)
import select                       # Módulo que permite esperar datos en varios sitios a la vez (teclado + socket)

# --- Comprobación de argumentos ---
if len(sys.argv) != 3:              # sys.argv es la lista de argumentos que se pasan al programa
    print(f"Uso: {sys.argv[0]} <puerto> <nick>")  # Muestra cómo se usa el programa correctamente
    sys.exit(1)                     # Sale del programa con código de error 1 (mal uso)

try:
    puerto = int(sys.argv[1])       # Convierte el primer argumento (el puerto) a número entero
except ValueError:                  # Si no puede convertirse (por ejemplo si pones “abc”)
    print("Puerto inválido.")       # Muestra mensaje de error
    sys.exit(1)                     # Sale del programa

nick = sys.argv[2]                  # Guarda el segundo argumento (tu nombre o apodo)

# --- Creación del socket UDP ---
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)  # Crea un socket de tipo UDP (no orientado a conexión)
s.bind(("", puerto))               # Lo asocia a tu puerto local, para poder recibir mensajes
destino = None                     # Variable para guardar a quién estás chateando (IP y puerto)

# El bloque try/finally sirve para que el socket se cierre siempre al final,
# incluso si ocurre un error o se interrumpe con Ctrl+C
try:
    while True:                    # Bucle principal: se repite hasta que escribas /QUIT o salgas
        print("> ", end="", flush=True)  # Muestra el símbolo ">" sin salto de línea (el prompt del chat)

        # Espera simultáneamente al teclado (sys.stdin) y al socket (s)
        # select.select devuelve una lista de los que tienen datos disponibles
        rlist, _, _ = select.select([s, sys.stdin], [], [])

        # Si hay datos en el socket UDP (es decir, te ha llegado un mensaje)
        if s in rlist:
            data, addr = s.recvfrom(65535)            # Recibe hasta 65535 bytes del remitente
            msg = data.decode("utf-8", errors="replace")  # Convierte los bytes a texto (cadena)
            print(f"\r{msg}\n", end="")               # \r borra el ">" de la línea actual, luego imprime el mensaje

        # Si hay algo escrito en el teclado
        if sys.stdin in rlist:
            linea = sys.stdin.readline()              # Lee una línea completa del teclado
            if not linea:                             # Si llega un EOF (Ctrl+D), salimos del bucle
                break

            linea = linea.strip()                     # Quita espacios o saltos de línea sobrantes

            # Si el usuario escribe /QUIT (comando para salir)
            if linea.upper().startswith("/QUIT"):     # .upper() convierte a mayúsculas (por si escribes /quit)
                if destino:                           # Si hay alguien conectado
                    # Envía un mensaje de aviso de desconexión
                    s.sendto(f"{nick}: <<se ha desconectado>>".encode("utf-8"), destino)
                break                                 # Sale del bucle principal (termina el programa)

            # Si el usuario escribe /CHAT <ip> <puerto>
            elif linea.upper().startswith("/CHAT"):
                partes = linea.split()                # Divide el texto por espacios
                if len(partes) != 3:                  # Si no hay justo 3 partes (/CHAT, ip, puerto)
                    print("Uso: /CHAT <ip> <puerto>") # Muestra el formato correcto
                else:
                    ip = partes[1]                    # Segunda parte: IP del otro usuario
                    try:
                        p = int(partes[2])            # Tercera parte: puerto del otro usuario
                        destino = (ip, p)             # Guarda el destino como una tupla (IP, puerto)
                        print(f"Destino fijado a {ip}:{p}")  # Confirma el destino
                    except ValueError:                # Si el puerto no es un número válido
                        print("Puerto inválido.")

            # Si no es un comando (es un mensaje normal)
            else:
                if not destino:                       # Si aún no has hecho /CHAT
                    print("Antes debes hacer /CHAT <ip> <puerto>")
                else:
                    # Prepara el mensaje con tu nick al principio y lo convierte a bytes
                    s.sendto(f"{nick}: {linea}".encode("utf-8"), destino)

# El bloque finally se ejecuta siempre, aunque haya errores o se use Ctrl+C
finally:
    s.close()                                        # Cierra el socket UDP para liberar el puerto
