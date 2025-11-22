# udp_servidor5_mejorado.py
import socket, sys, random

puerto = 9999
if len(sys.argv) > 1:
    puerto = int(sys.argv[1])

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("", puerto))

print(f"Servidor UDP mejorado escuchando en el puerto {puerto}")

# Guardamos los IDs ya procesados para evitar duplicados
procesados = set()

while True:
    datagrama, direccion = s.recvfrom(1024)
    mensaje = datagrama.decode("utf8")

    try:
        # Se espera formato "ID|mensaje"
        id_str, contenido = mensaje.split("|", 1)
        id_datagrama = int(id_str)
    except ValueError:
        print(f"Formato incorrecto recibido de {direccion}: {mensaje}")
        continue

    if id_datagrama in procesados:
        print(f"Duplicado recibido de {direccion} con ID {id_datagrama}, reenviando OK")
    else:
        print(f"Recibido [{id_datagrama}] de {direccion}: {contenido}")
        # Aquí iría la "acción real" (ejemplo: guardar en DB, procesar...)
        procesados.add(id_datagrama)

    # Enviamos confirmación con el ID
    s.sendto(f"OK {id_datagrama}".encode("utf8"), direccion)
