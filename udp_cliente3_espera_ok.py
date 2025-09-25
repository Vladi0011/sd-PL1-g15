# udp_cliente3_espera_ok.py
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

    s.settimeout(0.5)  # medio segundo
    try:
        datagrama, _ = s.recvfrom(1024)
        if datagrama.decode("utf8") == "OK":
            print("Recibida confirmación OK")
        else:
            print("Recibido mensaje inesperado")
    except socket.timeout:
        print("ERROR. No se recibió OK")
