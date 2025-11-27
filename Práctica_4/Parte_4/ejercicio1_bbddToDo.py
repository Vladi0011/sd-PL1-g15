from flask import Flask, jsonify, request, abort, make_response, url_for
import mysql.connector

app = Flask(__name__)


# CONFIGURACIÓN DE LA BASE DE DATOS

DB_CONFIG = {
    "host": "localhost",
    "user": "tarea_user",
    "password": "tarea_pass",
    "database": "tarea_db",
}



def get_db_connection():
    """
    Devuelve una conexión nueva a la base de datos.
    """
    return mysql.connector.connect(**DB_CONFIG)


def inicializar_bd():
    """
    Crea la tabla 'tareas' si no existe.
    """
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


# Llamamos a la inicialización al arrancar el módulo
inicializar_bd()


# FUNCIONES AUXILIARES


def fila_a_tarea(fila):
    """
    Convierte una fila de la BD (id, descripcion, completada)
    en un diccionario como los que usaba la lista original.
    """
    if fila is None:
        return None
    id_, descripcion, completada = fila
    return {
        "id": id_,
        "descripcion": descripcion,
        "completada": bool(completada),
    }


def buscar_tarea(id):
    """
    Busca una tarea por ID en la base de datos.
    Devuelve un diccionario o None si no existe.
    """
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
    """
    Convierte una tarea a formato HATEOAS.
    Cambia 'id' por 'uri' manteniendo el resto de campos.
    """
    nueva = {}
    for campo in tarea:
        if campo == "id":
            nueva["uri"] = url_for("obtener_tarea", id=tarea["id"], _external=True)
        else:
            nueva[campo] = tarea[campo]
    return nueva


def obtener_todas_las_tareas():
    """
    Devuelve una lista de todas las tareas (dicts) desde la BD.
    """
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, descripcion, completada FROM tareas")
    filas = cur.fetchall()
    cur.close()
    conn.close()
    return [fila_a_tarea(f) for f in filas]


def insertar_tarea(descripcion, completada=False):
    """
    Inserta una nueva tarea en la BD y devuelve la tarea completa.
    """
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
    """
    Actualiza los campos indicados de la tarea con ese id.
    Devuelve la tarea actualizada o None si no existe.
    """
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
    """
    Borra la tarea con ese id. Devuelve True si se borró,
    False si no existía.
    """
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM tareas WHERE id = %s", (id,))
    filas_afectadas = cur.rowcount
    conn.commit()
    cur.close()
    conn.close()
    return filas_afectadas > 0



# ENDPOINTS REST


@app.route("/lista/v1/tareas", methods=["GET"])
def obtener_tareas():
    tareas = obtener_todas_las_tareas()
    return jsonify({"tareas": [hacer_publica(t) for t in tareas]})


@app.route("/lista/v1/tarea/<int:id>", methods=["GET"])
def obtener_tarea(id):
    tarea = buscar_tarea(id)
    if tarea is None:
        abort(404)
    return jsonify(hacer_publica(tarea))


@app.route("/lista/v1/tareas", methods=["POST"])
def crear_tarea():
    if not request.json or "descripcion" not in request.json:
        abort(400)

    descripcion = request.json.get("descripcion")
    completada = request.json.get("completada", False)

    nueva_tarea = insertar_tarea(descripcion, completada)
    return jsonify(hacer_publica(nueva_tarea)), 201


@app.route("/lista/v1/tarea/<int:id>", methods=["PUT"])
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
    # Para pruebas rápidas con flask run / python, pero
    # en la práctica lo lanzarás con:
    #   gunicorn -w 1 ejercicio1_bbddToDo:app
    app.run(debug=True)
