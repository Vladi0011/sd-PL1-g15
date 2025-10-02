import socket
import sys
import time

broadcast_addr = "255.255.255.255"
puerto = 12345

if len(sys.argv) > 1:
    broadcast_addr = sys.argv[1]
if len(sys.argv) > 2:
    puerto = int(sys.argv[2])

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s.settimeout(3)

# Enviar broadcast
s.sendto("SERVICIO".encode("utf8"), (broadcast_addr, puerto))
print("Buscando servidores...")

# Recibir respuestas
servidores = []
try:
    while True:
        data, addr = s.recvfrom(1024)
        if data.decode("utf8") == "HOLA":
            servidores.append(addr)
            print(f"Servidor encontrado: {addr}")
except:
    pass

# Usar primer servidor
if servidores:
    print(f"Usando primer servidor: {servidores[0]}")
    s.sendto("HOLA cliente".encode("utf8"), servidores[0])
else:
    print("No se encontraron servidores")

s.close()