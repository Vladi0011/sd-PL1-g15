import socket
import time

servidor = "localhost"
puerto = 9999

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((servidor, puerto))

print("Enviando 5 mensajes de 'ABCD' (4 bytes cada uno)")
for i in range(5):
    mensaje = "ABCD"
    sock.sendall(mensaje.encode("ascii"))
    print(f"Enviado: {mensaje} ({len(mensaje)} bytes)")
    time.sleep(0.1)  # Pequeño retardo entre envíos

print("Enviando mensaje final: 'FINAL'")
sock.sendall("FINAL".encode("ascii"))
sock.close()
print("Conexión cerrada")