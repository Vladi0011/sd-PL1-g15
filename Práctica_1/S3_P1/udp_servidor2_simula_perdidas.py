# udp_servidor2_simula_perdidas.py
import socket, sys, random

puerto = 9999
if len(sys.argv) > 1:
    puerto = int(sys.argv[1])

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("", puerto))

print(f"Servidor UDP con pérdidas escuchando en el puerto {puerto}")

while True:
    datagrama, direccion = s.recvfrom(1024)
    if random.randint(0, 1) == 0:
        print("Simulando paquete perdido")
    else:
        print(f"Recibido de {direccion}: {datagrama.decode('utf8')}")
