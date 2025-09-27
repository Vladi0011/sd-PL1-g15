import socket

# Crear socket UDP para broadcast
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
sock.settimeout(2)

# Enviar "HOLA" a todos en la red
sock.sendto(b"HOLA", ("255.255.255.255", 12345))

# Esperar primera respuesta
try:
    data, addr = sock.recvfrom(1024)
    print(f"Servidor encontrado: {addr} -> {data.decode()}")
except socket.timeout:
    print("No se encontraron servidores")

sock.close()
