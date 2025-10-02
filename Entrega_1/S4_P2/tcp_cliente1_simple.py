import socket   # API de sockets TCP/IP
import sys      # argumentos de consola
import time     # pausas opcionales entre envíos

# lee host y puerto; defaults: localhost:9999
host = sys.argv[1] if len(sys.argv) > 1 else "localhost"
puerto = int(sys.argv[2]) if len(sys.argv) > 2 else 9999

# crea socket TCP del lado cliente
c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# establece la conexión con el servidor indicado
c.connect((host, puerto))

try:
    # envía cinco mensajes de tamaño fijo (5 bytes)
    for _ in range(5):
        c.sendall(b"ABCDE")     # manda exactamente 5 bytes
        # time.sleep(0.2)       # separar envíos (opcional)
    # envía palabra de finalización para cerrar ordenadamente
    c.sendall(b"FINAL")
finally:
    c.close()                   # cierra socket y libera recursos
