import socket   # API de sockets TCP/IP
import sys      # lectura de argumentos de consola

# toma puerto por CLI, o usa 9999 por defecto
puerto = int(sys.argv[1]) if len(sys.argv) > 1 else 9999

# crea socket TCP (IPv4, flujo fiable)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# asocia el socket a todas las IPs y al puerto
s.bind(("", puerto))
# pasa a modo pasivo; cola de espera de hasta 5
s.listen(5)

print(f"Escuchando en puerto {puerto} (mensajes de 5 bytes)")

while True:  # bucle principal: aceptar clientes sin fin
    print("Esperando un cliente…")
    sd, origen = s.accept()                 # bloquea hasta conexión entrante
    print(f"Conectado desde {origen}")      # muestra IP y puerto del cliente

    try:
        while True:                         # bucle de atención al cliente
            datos = sd.recv(5)              # lee exactamente 5 bytes máx.
            if not datos:                   # vacío ⇒ cliente cerró su socket
                print("Cliente cerró conexión inesperadamente")
                break
            # decodifica bytes recibidos como texto ASCII
            msg = datos.decode("ascii", errors="replace")

            if msg == "FINAL":              # palabra clave para terminar
                print("Recibido FINAL → cierro sesión con cliente")
                break

            print(f"Recibido bloque: {msg}")  # muestra bloque de 5 bytes
    finally:
        sd.close()                          # libera el socket de datos
        # vuelve al while exterior para aceptar otro cliente
