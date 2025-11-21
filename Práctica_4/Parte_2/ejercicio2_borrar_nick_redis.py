import redis
import sys

def borrar_clave(redis_host, redis_port, clave):
    try:
        # Crear conexión con Redis
        r = redis.Redis(host=redis_host, port=int(redis_port), decode_responses=True)

        # Intentar borrar la clave
        resultado = r.delete(clave)

        if resultado == 1:
            print(f"✅ La clave '{clave}' ha sido eliminada correctamente.")
        else:
            print(f"ℹ️ La clave '{clave}' no existía en Redis.")
    except Exception as e:
        print(f"❌ Error al conectar o borrar la clave: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Uso: python ejercicio2_borrar_nick_redis.py <IP> <PUERTO> <CLAVE>")
        sys.exit(1)

    ip = sys.argv[1]
    puerto = sys.argv[2]
    clave = sys.argv[3]

    borrar_clave(ip, puerto, clave)
