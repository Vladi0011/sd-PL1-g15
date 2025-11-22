import socket
import time

def recvall(sock, n):
    """Recibe exactamente n bytes o retorna None si la conexión se cierra"""
    data = b""
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data += packet
    return data

puerto = 9999

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("", puerto))
s.listen(1)

print(f"Servidor con recvall escuchando en puerto {puerto}")

while True:
    print("\nEsperando cliente...")
    sd, origen = s.accept()
    print(f"Cliente conectado desde {origen}")
    
    continuar = True
    mensaje_count = 0
    
    while continuar:
        datos = recvall(sd, 5)  # ¡ESPERA EXACTAMENTE 5 BYTES!
        
        if datos is None:
            print("Conexión cerrada inesperadamente")
            continuar = False
        else:
            mensaje_count += 1
            texto = datos.decode("ascii")
            print(f"Mensaje {mensaje_count}: '{texto}'")
            
            if texto == "FINAL":
                print("✓ Recibido mensaje FINAL correctamente")
                continuar = False
            elif "FINAL" in texto:
                print("✗ ¡FINAL detectado pero mezclado con otros datos!")
                continuar = False
    
    sd.close()
    print("Conexión con cliente cerrada")