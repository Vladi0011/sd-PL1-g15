# udp_cliente4_reintenta.py
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
    contador += 1

    timeout = 0.2  # empieza con 200 ms
    while True:
        s.sendto(mensaje.encode("utf8"), (host, puerto))
        s.settimeout(timeout)
        try:
            datagrama, _ = s.recvfrom(1024)
            if datagrama.decode("utf8") == "OK":
                print("Recibida confirmación OK")
                break  # sale del bucle de reintentos
        except socket.timeout:
            print(f"Timeout {timeout:.1f}s. Reintentando...")
            timeout *= 2
            if timeout > 2.0:
                print("Puede que el servidor esté caído. Inténtelo más tarde.")
                exit()
