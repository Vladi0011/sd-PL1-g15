
import redis
import os
import threading
import time

# Conexión a Redis
redis_host = os.getenv("REDIS_HOST", "localhost")
r = redis.Redis(host=redis_host, port=6379, db=0)

def calcular_fibonacci(n, job_id):
    """
    Genera Fibonacci(n) actualizando progreso en Redis
    """
    print(f"[{job_id}] Iniciando cálculo de Fibonacci({n})…")

    fib = [0, 1]
    if n == 0:
        fib = [0]
    elif n == 1:
        fib = [1]
    else:
        for i in range(2, n):
            fib.append(fib[-1] + fib[-2])

            # porcentaje = i/(n-1)
            progreso = int((i / (n - 1)) * 100)
            r.set(f"job:{job_id}:progress", progreso)

            time.sleep(0.3)  # para que tarde 20–30 segundos y se vea en vídeo

    # Guardar resultado como cadena "0 1 1 2..."
    resultado = " ".join(map(str, fib))
    r.set(f"job:{job_id}:result", resultado)
    r.set(f"job:{job_id}:progress", 100)

    print(f"[{job_id}] Cálculo completado.")

def procesar_trabajo(job_id):
    # Obtener parámetro n
    n = r.get(f"job:{job_id}:params")
    n = int(n.decode("utf-8"))

    calcular_fibonacci(n, job_id)


def main():
    print("Servidor de procesamiento iniciado. Esperando trabajos…")

    while True:
        job_id = r.blpop("trabajos")[1]
        job_id = job_id.decode("utf-8")

        print(f"Trabajo recibido: {job_id}")

        hilo = threading.Thread(target=procesar_trabajo, args=(job_id,))
        hilo.start()


if __name__ == "__main__":
    main()
