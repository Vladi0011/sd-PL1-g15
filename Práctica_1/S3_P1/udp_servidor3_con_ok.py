# udp_servidor3_con_ok.py
import socket, sys, random

puerto = 9999
if len(sys.argv) > 1:
    puerto = int(sys.argv[1])

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("", puerto))

print(f"Servidor UDP con OK escuchando en el puerto {puerto}")

while True:
    datagrama, direccion = s.recvfrom(1024)
    if random.randint(0, 1) == 0:
        print("Simulando paquete perdido")
    else:
        mensaje = datagrama.decode("utf8")
        print(f"Recibido de {direccion}: {mensaje}")
        s.sendto("OK".encode("utf8"), direccion)
