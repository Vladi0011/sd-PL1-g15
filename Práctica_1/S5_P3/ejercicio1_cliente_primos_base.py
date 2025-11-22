import sys                  # Módulo para leer argumentos de línea de comandos
import socket               # Módulo para crear y usar sockets TCP/UDP
import datetime             # Para imprimir la hora local junto a los mensajes

if len(sys.argv) != 4:      # Comprobación de argumentos: ip, puerto y cantidad
    print("Uso: cliente.py ip puerto cantidadPrimos")
    sys.exit(1)             # Salir si no hay el nº correcto de argumentos

ip_servidor = sys.argv[1]   # IP del servidor (p.ej., 127.0.0.1)
puerto_servidor = sys.argv[2]  # Puerto del servidor (p.ej., 9999)
cantidad = int(sys.argv[3])    # Cantidad de primos que queremos

# Crear el socket TCP
cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conectar al servidor en (ip, puerto)
cliente_socket.connect((ip_servidor, int(puerto_servidor)))

# Enviar al servidor la cantidad solicitada (como texto codificado a bytes)
cliente_socket.sendall(str(cantidad).encode())

# Bucle para recibir y mostrar mensajes del servidor
while True:
    data = cliente_socket.recv(1024).decode()  # Recibe hasta 1024 bytes y decodifica a str
    if not data:                               # Si no llega nada, conexión cerrada
        break

    hora_actual = datetime.datetime.now().time()  # Hora local para imprimir contexto
    print("La hora actual es:", hora_actual)
    # Imprime el mensaje; si no acaba en salto de línea, se lo añadimos
    print(data, end="" if data.endswith("\n") else "\n")

    # Si detecta el texto "FIN", el servidor ha terminado
    if "FIN" in data:
        cliente_socket.close()   # Cierra el socket del cliente
        break                    # Sale del bucle y termina el programa
