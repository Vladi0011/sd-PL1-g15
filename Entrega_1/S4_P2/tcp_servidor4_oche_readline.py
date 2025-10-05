import socket
import sys
import time

puerto = int(sys.argv[1]) if len(sys.argv) > 1 else 9999

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("", puerto))
s.listen(5)

print(f"Servidor OCHE escuchando en puerto {puerto}")

while True:
    print("Esperando un cliente…")
    sd, origen = s.accept()
    print(f"Conectado desde {origen}")
    
    time.sleep(1)
    
    f = sd.makefile(encoding="utf8", newline="\r\n")
    
    try:
        while True:
            mensaje = f.readline()
            if not mensaje:
                print("Cliente cerró conexión")
                break
            
            print(f"Recibido: {repr(mensaje)}")
            
            linea = mensaje[:-2]
            linea_invertida = linea[::-1]
            respuesta = linea_invertida + "\r\n"
            
            print(f"Enviando: {repr(respuesta)}")
            sd.sendall(respuesta.encode("utf8"))
    finally:
        f.close()
        sd.close()