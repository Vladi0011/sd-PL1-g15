
import uuid
import redis
import os
from flask import Flask, jsonify, request, make_response
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import check_password_hash


# Configuración de Flask + Redis

app = Flask(__name__)

redis_host = os.getenv("REDIS_HOST", "localhost")
r = redis.Redis(host=redis_host, port=6379, db=0)



# Cargar usuarios autorizados desde un fichero

auth = HTTPBasicAuth()
auth.realm = "Es necesario autenticarse"

autorizados = {}

def leer_usuarios(fichero):
    try:
        with open(fichero, "r") as f:
            for linea in f.readlines():
                linea = linea.strip()
                if not linea:
                    continue
                usuario, hash_clave = linea.split()
                autorizados[usuario] = hash_clave
    except:
        print("No se pudo leer el fichero de contraseñas")

# Carga desde contraseñas.txt (123)
leer_usuarios("c.txt")



@auth.verify_password
def verificar(usuario, contraseña):
    """
    Verifica usuario usando hashes seguros.
    """
    if usuario in autorizados:
        hash_guardado = autorizados[usuario]
        return check_password_hash(hash_guardado, contraseña)
    return False


@auth.error_handler
def no_autorizado():
    return make_response(jsonify({"error": "Credenciales no válidas"}), 401)



# Funciones auxiliares


def crear_job_id():
    return str(uuid.uuid4())


def obtener_estado(job_id):
    """
    Devuelve progreso y, si existe, resultado.
    """
    progreso = r.get(f"job:{job_id}:progress")
    resultado = r.get(f"job:{job_id}:result")

    if progreso is None:
        return None  # no existe

    progreso = int(progreso.decode("utf-8"))

    if resultado:
        # Convertir "0 1 1 2 3..." en lista de enteros
        lista = resultado.decode("utf-8").split()
        lista = list(map(int, lista))
        return {
            "job_id": job_id,
            "progreso": progreso,
            "resultado": lista
        }

    return {
        "job_id": job_id,
        "progreso": progreso
    }


@app.route("/fibo", methods=["POST"])
@auth.login_required
def nuevo_trabajo():
    """
    Crea un nuevo trabajo de cálculo Fibonacci(n).
    """
    if not request.json or "n" not in request.json:
        return make_response(jsonify({"error": "JSON inválido, falta n"}), 400)

    n = request.json["n"]

    if type(n) != int or n <= 0:
        return make_response(jsonify({"error": "n debe ser entero positivo"}), 400)

    # Crear ID del trabajo
    job_id = crear_job_id()

    # Guardar parámetros en Redis
    r.set(f"job:{job_id}:params", n)
    r.set(f"job:{job_id}:progress", 0)

    # Enviar trabajo a la cola
    r.rpush("trabajos", job_id)

    print(f"[API] Trabajo enviado: {job_id} (n={n})")

    return jsonify({
        "job_id": job_id,
        "progreso": 0,
        "mensaje": "Trabajo en cola. Consulta /fibo/<job_id>"
    }), 202



@app.route("/fibo/<job_id>", methods=["GET"])
@auth.login_required
def estado_trabajo(job_id):
    """
    Devuelve progreso y resultado (si finalizado).
    """
    estado = obtener_estado(job_id)

    if estado is None:
        return make_response(jsonify({"error": "ID no encontrado"}), 404)

    return jsonify(estado), 200



# Manejadores de errores globales

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"error": "No encontrado"}), 404)


@app.errorhandler(405)
def metodo_no_valido(error):
    return make_response(jsonify({"error": "Método no permitido"}), 405)


@app.errorhandler(500)
def error_servidor(error):
    return make_response(jsonify({"error": "Error interno de servidor"}), 500)



# pruebas(sera ignorado por el docker)

if __name__ == "__main__":
    # Para pruebas locales sin gunicorn
    app.run(host="0.0.0.0", port=5000)
