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

    s.settimeout(0.5)  # medio segundo de espera
    try:    # esperar OK del servidor con timeout de 0.5 segundos 
        datagrama, _ = s.recvfrom(1024)     # buffer de 1K bytes , si no llega en 0.5 seg se lanza excepción socket.timeout 
        if datagrama.decode("utf8") == "OK":
            print("Recibida confirmación OK")
        else:
            print("Recibido mensaje inesperado")
    except socket.timeout:
        print("ERROR. No se recibió OK")
