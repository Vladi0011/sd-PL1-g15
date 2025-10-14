# -*- coding: utf-8 -*-
"""
ejercicio2_servidor_primos_threading.py
Servidor TCP concurrente (paralelo) con hilos para calcular números primos.
Cada conexión de cliente se atiende en un hilo independiente.
El código está explicado con comentarios línea a línea.
"""

import sys                      # Para leer el argumento del puerto desde la línea de comandos
import socket                   # Para crear sockets TCP/IPv4
import time                     # Para introducir esperas y simular carga de CPU
import threading                # Para crear y gestionar hilos de ejecución


def es_primo(numero: int) -> bool:
    """Devuelve True si 'numero' es primo; False en caso contrario."""
    if numero < 2:             # 0 y 1 no son primos
        return False
    for i in range(2, numero): # Recorremos posibles divisores desde 2 hasta n-1
        time.sleep(0.1)        # Pausa artificial para visualizar la concurrencia
        if numero % i == 0:    # Si es divisible por 'i', no es primo
            return False
    return True                # Si no es divisible por ninguno, entonces es primo


def calcular_cliente(num_hilo: int, cliente_socket: socket.socket, cliente_address):
    """
    Función que ejecuta CADA HILO.
    Atiende a un cliente: recibe la cantidad, calcula primos y envía progreso/lista.
    """
    print(f"Soy el hilo {num_hilo}")  # Identificador de hilo para el log del servidor

    try:
        data = cliente_socket.recv(1024).decode()  # Recibe del cliente la cantidad solicitada
        numero = int(data)                         # Convierte el texto recibido a entero
    except Exception:                               # Si falla (desconexión o dato inválido)
        try:
            cliente_socket.sendall("Solicitud inválida\nFIN".encode())  # Informa al cliente
        finally:
            cliente_socket.close()                 # Cierra el socket de ese cliente
        return                                     # Termina el hilo

    print(f"[Hilo {num_hilo}] Calculando los primeros {numero} números primos...")

    primos = []                # Lista donde acumularemos los números primos encontrados
    candidato = 2              # Primer número a evaluar como primo

    # Bucle principal de cálculo hasta reunir 'numero' primos
    while len(primos) < numero:
        if es_primo(candidato):                   # Si el candidato es primo...
            primos.append(candidato)              # ...lo añadimos a la lista
            # Cada 5 primos (o al terminar) notificamos progreso al cliente
            if len(primos) % 5 == 0 or len(primos) == numero:
                mensaje_parcial = (
                    f"Se han calculado {len(primos)} de los {numero} números primos solicitados\n"
                )
                cliente_socket.sendall(mensaje_parcial.encode())  # Envío parcial
        candidato += 1                            # Probamos el siguiente número

    # Cuando terminamos, enviamos la lista completa
    mensaje_final = "Primos: " + str(primos) + "\n"
    cliente_socket.sendall(mensaje_final.encode())

    # Enviamos marca de finalización y cerramos la conexión de este cliente
    cliente_socket.sendall("FIN".encode())
    cliente_socket.close()
    print(f"[Hilo {num_hilo}] Conexión cerrada con: {cliente_address}")


# ---------- Punto de entrada del proceso (hilo principal) ----------

if len(sys.argv) != 2:                             # Validamos que nos pasen 1 argumento (puerto)
    print("Uso: servidor_threading.py puerto")
    sys.exit(1)                                    # Salimos si los argumentos son incorrectos

puerto_servidor = int(sys.argv[1])                 # Convertimos el puerto de str a int

servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Creamos socket TCP/IPv4
servidor_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Permitimos reutilizar el puerto
servidor_socket.bind(("", puerto_servidor))        # Asociamos el socket a todas las interfaces y al puerto
servidor_socket.listen(8)                          # Ponemos el socket a escuchar (cola máx. 8 clientes)

print("El servidor está listo para recibir conexiones en el puerto", puerto_servidor)

num_hilo = 0                                       # Contador para numerar hilos que vamos creando

# Bucle infinito: el hilo principal SOLO acepta nuevas conexiones
while True:
    print("- Hilo principal esperando cliente -")  # Mensaje de estado antes de aceptar
    cliente_socket, cliente_address = servidor_socket.accept()  # Bloquea hasta que llega un cliente
    print("Conexión establecida desde:", cliente_address)

    # Creamos un nuevo hilo para atender a este cliente sin bloquear al principal
    cliente_thread = threading.Thread(
        target=calcular_cliente,                   # Función que ejecutará el hilo
        args=(num_hilo, cliente_socket, cliente_address),  # Parámetros de esa función
        daemon=True                                # Hilo en modo 'daemon' (no bloquea salida del proceso)
    )
    cliente_thread.start()                         # Lanzamos el hilo: empieza a ejecutar calcular_cliente
    num_hilo += 1                                  # Actualizamos el contador para el próximo hilo
