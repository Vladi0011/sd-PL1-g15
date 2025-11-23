from flask import Flask, jsonify, abort, make_response, request

app = Flask(__name__)

# Datos iniciales
tareas = [
    {'id': 1, 'descripcion': 'Tarea 1', 'completada': True},
    {'id': 2, 'descripcion': 'Tarea 2', 'completada': False}
]

def buscar_tarea(id):
    for t in tareas:
        if t['id'] == id:
            return t
    return None

# Rutas GET (necesarias para que el servidor funcione normal)
@app.route("/lista/v1/tareas", methods=["GET"])
def get_tareas():
    return jsonify({"tareas": tareas})

@app.route('/lista/v1/tarea/<int:id>', methods=["GET"])
def get_tarea(id):
    tarea = buscar_tarea(id)
    if tarea is None:
        abort(404)
    return jsonify({'tarea': tarea})

# --- PARTE DEL EXPERIMENTO 3 ---
@app.route("/lista/v1/tareas", methods=["POST"])
def create_tarea():
    print("Recibido POST con datos:")
    print(request.data)  # Imprimimos los bytes brutos
    print("-------")
    return "OK", 201
# -------------------------------

@app.errorhandler(404)
def no_encontrado(error):
    return make_response(jsonify({'error': 'Tarea inexistente'}), 404)

if __name__ == "__main__":
    app.run(debug=True)