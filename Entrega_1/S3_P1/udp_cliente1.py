# udp_cliente1.py
import socket, sys

host = "localhost"
puerto = 9999
if len(sys.argv) > 1:   # Si se proporciona un argumento, usarlo como host 
    host = sys.argv[1]
if len(sys.argv) > 2:   # Si se proporciona un segundo argumento, usarlo como puerto 
    puerto = int(sys.argv[2])

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    linea = input("Escribe mensaje (FIN para terminar): ")
    if linea == "FIN":
        break
    s.sendto(linea.encode("utf8"), (host, puerto))
