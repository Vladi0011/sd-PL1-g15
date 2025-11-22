# udp_cliente2_numera_mensajes.py
import socket, sys

host = "localhost"
puerto = 9999
if len(sys.argv) > 1:
    host = sys.argv[1]
if len(sys.argv) > 2:
    puerto = int(sys.argv[2])

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
contador = 1

while True:
    linea = input("Escribe mensaje (FIN para terminar): ")
    if linea == "FIN":
        break
    mensaje = f"{contador}: {linea}"
    s.sendto(mensaje.encode("utf8"), (host, puerto))
    contador += 1
