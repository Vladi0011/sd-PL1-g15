import socket
import sys

puerto = 12345
if len(sys.argv) > 1:
    puerto = int(sys.argv[1])

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s.bind(('', puerto))

print(f"Servidor escuchando en puerto {puerto}")

while True:
    data, addr = s.recvfrom(1024)
    mensaje = data.decode("utf8")
    
    if mensaje == "SERVICIO":
        s.sendto("HOLA".encode("utf8"), addr)
        print(f"Respondido HOLA a {addr}")
