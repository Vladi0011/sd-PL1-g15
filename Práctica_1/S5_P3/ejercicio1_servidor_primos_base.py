import sys                     # Para leer argumentos (el puerto de escucha)
import socket                  # Para crear el socket TCP del servidor
import time                    # Para dormir y ralentizar el cálculo (efecto docente)

def es_primo(numero: int) -> bool:
    if numero < 2:             # 0 y 1 no son primos
        return False
    for i in range(2, numero): # Prueba divisores desde 2 hasta n-1
        time.sleep(0.1)        # Pausa intencionada para notar el progreso
        if numero % i == 0:    # Si es divisible por i, no es primo
            return False
    return True                # Si no fue divisible por ninguno, es primo

# Validación de argumentos: debe venir sólo el puerto
if len(sys.argv) != 2:
    print("Uso: servidor.py puerto")
    sys.exit(1)

puerto_servidor = int(sys.argv[1])  # Puerto TCP donde el servidor escuchará

# Crear el socket TCP IPv4
servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Permite reutilizar el puerto tras reinicios rápidos del servidor
servidor_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Asocia el socket a todas las interfaces locales ("") y al puerto indicado
servidor_socket.bind(("", puerto_servidor))

# Comienza a escuchar conexiones entrantes (cola máx. 4)
servidor_socket.listen(4)

print("El servidor está listo para recibir conexiones en el puerto", puerto_servidor)

while True:                                     # Servidor iterativo: atiende 1 cliente cada vez
    print("- Esperando cliente -")              # Mensaje de estado
    cliente_socket, cliente_address = servidor_socket.accept()  # Bloquea hasta que entra un cliente
    print("Conexión establecida desde:", cliente_address)

    # Recibe del cliente la cantidad de primos solicitados
    data = cliente_socket.recv(1024).decode()
    try:
        numero = int(data)                      # Convierte a entero
    except ValueError:                          # Si llega algo no numérico:
        cliente_socket.sendall("Solicitud inválida\nFIN".encode())
        cliente_socket.close()
        continue                                # Vuelve a esperar otro cliente

    print(f"Calculando los primeros {numero} números primos...")

    # Inicializa cálculo de primos
    primos = []                                 # Lista resultado
    candidato = 2                               # Primer número a probar

    while len(primos) < numero:                 # Hasta completar la cantidad pedida
        if es_primo(candidato):                 # Si el candidato es primo...
            primos.append(candidato)            # ...lo añadimos
            # Envia un mensaje de progreso cada 5 primos o al terminar
            if len(primos) % 5 == 0 or len(primos) == numero:
                mensaje_parcial = (
                    f"Se han calculado {len(primos)} de los {numero} números primos solicitados\n"
                )
                cliente_socket.sendall(mensaje_parcial.encode())
        candidato += 1                          # Prueba el siguiente número

    # Cuando termina, envía la lista completa
    mensaje = "Primos: " + str(primos) + "\n"
    cliente_socket.sendall(mensaje.encode())

    # Señal de fin y cierre de conexión con el cliente
    cliente_socket.sendall("FIN".encode())
    cliente_socket.close()
    print("Conexión cerrada con:", cliente_address)

