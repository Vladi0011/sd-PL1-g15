import socket
import sys

host = sys.argv[1] if len(sys.argv) > 1 else "localhost"
puerto = int(sys.argv[2]) if len(sys.argv) > 2 else 9999

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

c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
c.connect((host, puerto))

mensajes = ["HOLA", "MUNDO", "PYTHON", "SOCKETS"]

try:
    for mensaje in mensajes:
        mensaje_bytes = mensaje.encode("utf8")
        longitud = str(len(mensaje_bytes)) + "\n"

        # Cabio para un unico mensaje
        paquete = longitud.encode("utf8") + mensaje_bytes
        print(f"Enviando (longitud+mensaje) en un solo sendall: {repr(longitud)}{repr(mensaje)}")
        c.sendall(paquete)

        longitud_respuesta = recibe_longitud(c)
        if longitud_respuesta is None:
            break
        
        respuesta_bytes = c.recv(longitud_respuesta)
        respuesta = respuesta_bytes.decode("utf8", errors="replace")
        print(f"Recibido: {repr(respuesta)}")
finally:
    c.close()
    print("Cliente terminado")


