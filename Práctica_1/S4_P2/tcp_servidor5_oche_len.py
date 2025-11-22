import socket
import sys

puerto = int(sys.argv[1]) if len(sys.argv) > 1 else 9999

def recvall(sock, n):
    data = b""
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet: return None
        data += packet
    return data

def recibe_longitud(sd):
    longitud_str = ""
    while True:
        byte = sd.recv(1)
        if not byte:
            return None
        char = byte.decode("utf8", errors="replace")
        if char == "\n":
            break
        longitud_str += char
    
    return int(longitud_str)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("", puerto))
s.listen(5)

print(f"Servidor OCHE escuchando en puerto {puerto}")

while True:
    print("Esperando un cliente…")
    sd, origen = s.accept()
    print(f"Conectado desde {origen}")

    try:
        while True:
            longitud = recibe_longitud(sd)
            if longitud is None:
                print("Cliente cerró conexión")
                break
            
            mensaje_bytes = sd.recvall(longitud)
            if not mensaje_bytes:
                print("Cliente cerró conexión")
                break
            
            mensaje = mensaje_bytes.decode("utf8", errors="replace")
            print(f"Recibido: {repr(mensaje)}")
            
            linea_invertida = mensaje[::-1]
            respuesta = linea_invertida
            respuesta_bytes = respuesta.encode("utf8")
            longitud_respuesta = str(len(respuesta_bytes)) + "\n"

            #  Cabio para un unico mensaje
            paquete_respuesta = longitud_respuesta.encode("utf8") + respuesta_bytes
            print(f"Enviando (longitud+mensaje) en un solo sendall: {repr(longitud_respuesta)}{repr(respuesta)}")
            sd.sendall(paquete_respuesta)

    finally:
        sd.close()

