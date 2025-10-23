import socket
import sys

puerto = int(sys.argv[1]) if len(sys.argv) > 1 else 9999

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
            
            mensaje_bytes = sd.recv(longitud)
            if not mensaje_bytes:
                print("Cliente cerró conexión")
                break
            
            mensaje = mensaje_bytes.decode("utf8", errors="replace")
            print(f"Recibido: {repr(mensaje)}")
            
            linea_invertida = mensaje[::-1]
            respuesta = linea_invertida
            respuesta_bytes = respuesta.encode("utf8")
            longitud_respuesta = str(len(respuesta_bytes)) + "\n"
            
            print(f"Enviando longitud: {repr(longitud_respuesta)}")
            sd.sendall(longitud_respuesta.encode("utf8"))
            print(f"Enviando mensaje: {repr(respuesta)}")
            sd.sendall(respuesta_bytes) 

    # CAMBIAR un sendall en vez de 2: FALLO GRAVE
    finally:

        sd.close()
