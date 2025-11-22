import socket
import sys

host = sys.argv[1] if len(sys.argv) > 1 else "localhost"
puerto = int(sys.argv[2]) if len(sys.argv) > 2 else 9999

c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
c.connect((host, puerto))

f = c.makefile(encoding="utf8", newline="\r\n")

mensajes = ["HOLA\r\n", "MUNDO\r\n", "PYTHON\r\n", "SOCKETS\r\n"]

try:
    for mensaje in mensajes:
        print(f"Enviando: {repr(mensaje)}")
        c.sendall(mensaje.encode("utf8"))
        
        respuesta = f.readline()
        print(f"Recibido: {repr(respuesta)}")
finally:
    f.close()
    c.close()
    print("Cliente terminado")