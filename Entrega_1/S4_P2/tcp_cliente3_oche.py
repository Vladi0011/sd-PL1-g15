import socket
import sys

host = sys.argv[1] if len(sys.argv) > 1 else "localhost"
puerto = int(sys.argv[2]) if len(sys.argv) > 2 else 9999

c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
c.connect((host, puerto))

mensajes = ["HOLA\r\n", "MUNDO\r\n", "PYTHON\r\n", "SOCKETS\r\n"]

try:
    for mensaje in mensajes:
        print(f"Enviando: {repr(mensaje)}")
        c.sendall(mensaje.encode("utf8"))
        
        respuesta = c.recv(80)
        respuesta_str = respuesta.decode("utf8", errors="replace")
        print(f"Recibido: {repr(respuesta_str)}")
finally:
    c.close()
    print("Cliente terminado")