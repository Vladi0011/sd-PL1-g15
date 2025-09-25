# udp_servidor1.py
import socket, sys

# Puerto por defecto
puerto = 9999
if len(sys.argv) > 1:
    puerto = int(sys.argv[1])

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("", puerto))  # "" = todas las interfaces

print(f"Servidor UDP escuchando en el puerto {puerto}")

while True:
    datagrama, direccion = s.recvfrom(1024)
    print(f"Recibido de {direccion}: {datagrama.decode('utf8')}")
