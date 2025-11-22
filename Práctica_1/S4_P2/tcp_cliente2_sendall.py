import socket
import sys
import time

host  = sys.argv[1] if len(sys.argv) > 1 else "localhost"
puerto = int(sys.argv[2]) if len(sys.argv) > 2 else 9999

c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # socket TCP
c.connect((host, puerto))                              # conectar

try:
    for _ in range(5):            # cinco mensajes
        c.sendall(b"ABCDE")       # enviar todo (5B)
        time.sleep(0.2)         # separar envíos (opcional)
    c.sendall(b"FINAL")           # señal de fin (5B)
finally:
    c.close()                     # cerrar socket
