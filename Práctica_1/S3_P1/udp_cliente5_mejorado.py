# udp_cliente5_mejorado.py
import socket, sys, random

host = "localhost"
puerto = 9999
if len(sys.argv) > 1:
    host = sys.argv[1]
if len(sys.argv) > 2:
    puerto = int(sys.argv[2])

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect((host, puerto))  # Filtra para que solo reciba del servidor
contador = 1

while True:
    linea = input("Escribe mensaje (FIN para terminar): ")
    if linea == "FIN":
        break

    # Generamos un identificador aleatorio para el mensaje
    id_msg = random.randint(1000, 9999)
    mensaje = f"{id_msg}|{linea}"

    timeout = 0.2
    while True:
        s.send(mensaje.encode("utf8"))
        s.settimeout(timeout)

        try:
            respuesta = s.recv(1024).decode("utf8")
            if respuesta == f"OK {id_msg}":
                print(f"Confirmación recibida para ID {id_msg}")
                break
            else:
                print(f"Respuesta inesperada: {respuesta}")
        except socket.timeout:
            print(f"Timeout {timeout:.1f}s. Reintentando...")
            timeout *= 2
            if timeout > 2.0:
                print("Servidor no responde. Abortando.")
                exit()
