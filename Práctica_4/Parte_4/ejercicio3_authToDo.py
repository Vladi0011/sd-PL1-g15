from flask import Flask, jsonify, request, abort, make_response, url_for
import mysql.connector
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)

# AUTENTICACIÓN HTTP BÁSICA

auth = HTTPBasicAuth()
auth.realm = "Es necesario autenticarse"


# Único usuario permitido: "alumno" con clave "alumno_pass"
@auth.verify_password
def verificar(usuario, contraseña):
    if usuario == "alumno" and contraseña == "alumno_pass":
        return True
    else:
        return False


@auth.error_handler
def no_autorizado():
    return make_response(jsonify({'error': 'Credenciales no válidas'}), 401)


# CONFIGURACIÓN DE LA BASE DE DATOS

DB_CONFIG = {
    "host": "localhost",
    "user": "tarea_user",
    "password": "tarea_pass",  # el usuario/clave que creaste en MariaDB
    "database": "tarea_db",
}


def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)


def inicializar_bd():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS tareas (
            id INT AUTO_INCREMENT PRIMARY KEY,
            descripcion VARCHAR(255) NOT NULL,
            completada BOOLEAN NOT NULL DEFAULT 0
        )
        """
    )
    conn.commit()
    cur.close()
    conn.close()


inicializar_bd()

# FUNCIONES AUXILIARES


def fila_a_tarea(fila):
    if fila is None:
        return None
    id_, descripcion, completada = fila
    return {
        "id": id_,
        "descripcion": descripcion,
        "completada": bool(completada),
    }


def buscar_tarea(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, descripcion, completada FROM tareas WHERE id = %s",
        (id,),
    )
    fila = cur.fetchone()
    cur.close()
    conn.close()
    return fila_a_tarea(fila)


def hacer_publica(tarea):
    nueva = {}
    for campo in tarea:
        if campo == "id":
            nueva["uri"] = url_for("obtener_tarea", id=tarea["id"], _external=True)
        else:
            nueva[campo] = tarea[campo]
    return nueva


def obtener_todas_las_tareas():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, descripcion, completada FROM tareas")
    filas = cur.fetchall()
    cur.close()
    conn.close()
    return [fila_a_tarea(f) for f in filas]


def insertar_tarea(descripcion, completada=False):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO tareas (descripcion, completada) VALUES (%s, %s)",
        (descripcion, int(bool(completada))),
    )
    conn.commit()
    id_nueva = cur.lastrowid
    cur.close()
    conn.close()
    return buscar_tarea(id_nueva)


def actualizar_tarea(id, descripcion=None, completada=None):
    tarea_actual = buscar_tarea(id)
    if tarea_actual is None:
        return None

    nueva_desc = descripcion if descripcion is not None else tarea_actual["descripcion"]
    nueva_comp = (
        bool(completada)
        if completada is not None
        else bool(tarea_actual["completada"])
    )

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """
        UPDATE tareas
        SET descripcion = %s, completada = %s
        WHERE id = %s
        """,
        (nueva_desc, int(nueva_comp), id),
    )
    conn.commit()
    cur.close()
    conn.close()

    return buscar_tarea(id)


def borrar_tarea(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM tareas WHERE id = %s", (id,))
    filas_afectadas = cur.rowcount
    conn.commit()
    cur.close()
    conn.close()
    return filas_afectadas > 0

# ENDPOINTS REST PROTEGIDOS CON AUTENTICACIÓN


@app.route("/lista/v1/tareas", methods=["GET"])
@auth.login_required
def obtener_tareas():
    tareas = obtener_todas_las_tareas()
    return jsonify({"tareas": [hacer_publica(t) for t in tareas]})


@app.route("/lista/v1/tarea/<int:id>", methods=["GET"])
@auth.login_required
def obtener_tarea(id):
    tarea = buscar_tarea(id)
    if tarea is None:
        abort(404)
    return jsonify(hacer_publica(tarea))


@app.route("/lista/v1/tareas", methods=["POST"])
@auth.login_required
def crear_tarea():
    if not request.json or "descripcion" not in request.json:
        abort(400)

    descripcion = request.json.get("descripcion")
    completada = request.json.get("completada", False)

    nueva_tarea = insertar_tarea(descripcion, completada)
    return jsonify(hacer_publica(nueva_tarea)), 201


@app.route("/lista/v1/tarea/<int:id>", methods=["PUT"])
@auth.login_required
def modificar_tarea(id):
    if not request.json:
        abort(400)

    tarea = buscar_tarea(id)
    if tarea is None:
        abort(404)

    descripcion = request.json.get("descripcion", tarea["descripcion"])
    completada = request.json.get("completada", tarea["completada"])

    tarea_actualizada = actualizar_tarea(id, descripcion, completada)
    return jsonify(hacer_publica(tarea_actualizada))


@app.route("/lista/v1/tarea/<int:id>", methods=["DELETE"])
@auth.login_required
def eliminar_tarea(id):
    tarea = buscar_tarea(id)
    if tarea is None:
        abort(404)

    borrado = borrar_tarea(id)
    if not borrado:
        abort(404)

    return jsonify({"borrado": True})

# MANEJADORES DE ERROR


@app.errorhandler(404)
def no_encontrado(error):
    return make_response(jsonify({"error": "Tarea inexistente"}), 404)


@app.errorhandler(400)
def solicitud_invalida(error):
    return make_response(jsonify({"error": "Solicitud incorrecta"}), 400)


if __name__ == "__main__":
    app.run(debug=True)
