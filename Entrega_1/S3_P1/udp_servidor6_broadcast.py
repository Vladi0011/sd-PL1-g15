import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("", 12345))

print("Servidor esperando mensajes...")

while True:
    data, addr = sock.recvfrom(1024)
    mensaje = data.decode()
    print(f"Recibido: {mensaje} de {addr}")
    
    if mensaje == "HOLA":
        sock.sendto(b"SERVIDOR ACTIVO", addr)
