import socket
import sys

puerto = int(sys.argv[1]) if len(sys.argv) > 1 else 9999

def recvall(sock, n):
    buf = bytearray()                 # acumulador de bytes
    while len(buf) < n:               # hasta completar n
        parte = sock.recv(n - len(buf))  # pide faltantes
        if not parte:                 # remoto cerró
            break
        buf.extend(parte)             # acumula recibidos
    return buf.decode("ascii", errors="replace")  # a texto

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)   # reutilizar puerto
s.bind(("", puerto))                                       # bind a puerto
s.listen(5)                                                # modo pasivo
print(f"Escuchando en {puerto} (recvall de 5 bytes)")

while True:                                                # aceptar siempre
    sd, origen = s.accept()                                # nueva sesión
    print(f"Conectado desde {origen}")
    try:
        while True:                                        # atender sesión
            msg = recvall(sd, 5)                           # leer 5 exactos
            if not msg:                                    # cierre remoto
                print("Cliente cerró conexión")
                break
            if msg == "FINAL":                             # token de fin
                print("Recibido FINAL → cerrar")
                break
            print(f"Recibido bloque: {msg}")               # mostrar bloque
    finally:
        sd.close()                                         # cerrar datos
