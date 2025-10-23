# -*- coding: utf-8 -*-
"""
ejercicio3_servidor_primos_fork.py
Servidor TCP concurrente mediante **procesos** usando os.fork().
El proceso padre acepta conexiones y, por cada cliente, crea un proceso hijo
que atiende esa conexión de principio a fin.
Todo está explicado con comentarios línea a línea.
"""

import os                       # Para usar os.fork() y os._exit()
import sys                      # Para leer el puerto desde la línea de comandos
import socket                   # Para crear y manejar sockets TCP
import time                     # Para introducir pausas (simular carga de CPU)


def es_primo(numero: int) -> bool:
    """Devuelve True si 'numero' es primo; False en caso contrario."""
    if numero < 2:             # 0 y 1 no son primos
        return False
    for i in range(2, numero): # Recorre posibles divisores desde 2 hasta n-1
        time.sleep(0.1)        # Pausa artificial para apreciar la concurrencia
        if numero % i == 0:    # Si es divisible por 'i', no es primo
            return False
    return True                # Si no fue divisible por ninguno, es primo


def calcular_cliente(cliente_socket: socket.socket, cliente_address):
    """
    Lógica completa que debe ejecutar **cada proceso hijo** para un cliente:
    recibir cantidad, calcular primos, enviar progreso/lista y cerrar.
    """
    try:
        data = cliente_socket.recv(1024).decode()   # Recibe la cantidad solicitada
        numero = int(data)                          # Intenta convertir a entero
    except Exception:
        try:
            cliente_socket.sendall("Solicitud inválida\nFIN".encode())
        finally:
            cliente_socket.close()
        return                                      # Termina la función en el hijo

    print(f"[Hijo {os.getpid()}] Calculando los primeros {numero} números primos...")

    primos = []                 # Lista de resultados
    candidato = 2               # Primer número a evaluar

    while len(primos) < numero: # Bucle hasta reunir todos los primos pedidos
        if es_primo(candidato): # Si el candidato es primo...
            primos.append(candidato)
            # Enviar progreso cada 5 primos o al terminar
            if len(primos) % 5 == 0 or len(primos) == numero:
                parcial = f"Se han calculado {len(primos)} de los {numero} números primos solicitados\n"
                cliente_socket.sendall(parcial.encode())
        candidato += 1

    # Enviar la lista final y el marcador de fin
    cliente_socket.sendall(("Primos: " + str(primos) + "\n").encode())
    cliente_socket.sendall("FIN".encode())
    cliente_socket.close()      # Cerrar el socket de datos en el hijo
    print(f"[Hijo {os.getpid()}] Conexión cerrada con: {cliente_address}")


# PUNTO DE ENTRADA DEL PROCESO PADRE

if len(sys.argv) != 2:                               # Validar nº de argumentos
    print("Uso: servidor_fork.py puerto")
    sys.exit(1)

puerto_servidor = int(sys.argv[1])                   # Puerto de escucha

# Crear socket pasivo (escucha) TCP/IPv4 en el padre
servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Reutilizar puerto
servidor_socket.bind(("", puerto_servidor))          # Asociar a todas las interfaces
servidor_socket.listen(8)                            # Escuchar con cola máxima 8

print("El servidor está listo para recibir conexiones en el puerto", puerto_servidor)

# Bucle infinito: aceptar conexiones y bifurcar proceso
while True:
    print("- Proceso padre esperando cliente -")
    cliente_socket, cliente_address = servidor_socket.accept()  # Acepta una conexión (bloqueante)
    print("Conexión establecida desde:", cliente_address)

    pid = os.fork()                                   # Crea un nuevo proceso (hijo)
    if pid == 0:
        # --- Estamos en el PROCESO HIJO ---
        # MUY IMPORTANTE: el hijo **no** necesita el socket pasivo de escucha
        servidor_socket.close()                       # Cerrar el socket pasivo en el hijo
        try:
            calcular_cliente(cliente_socket, cliente_address)  # Atiende al cliente
        finally:
            # Asegurar que el socket de datos esté cerrado y terminar el hijo
            try:
                cliente_socket.close()
            except Exception:
                pass
            os._exit(0)                               # Salir del hijo sin ejecutar atexit/flush del padre
    else:
        # Estamos en el PROCESO PADRE
        # El padre no usará el socket de datos de este cliente: debe cerrarlo inmediatamente.
        cliente_socket.close()                        # Cierre en el padre (evita fds abiertos)
        # El padre vuelve al bucle para aceptar otros clientes en paralelo con el hijo
