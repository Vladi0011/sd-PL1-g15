from flask import Flask, jsonify, abort, make_response

app = Flask(__name__)

tareas = [
    {'id': 1, 'descripcion': 'Tarea 1', 'completada': True}
]

def buscar_tarea(id):
    for t in tareas:
        if t['id'] == id:
            return t
    return None

@app.route('/lista/v1/tarea/<int:id>', methods=["GET"])
def get_tarea(id):
    tarea = buscar_tarea(id)
    if tarea is None:
        abort(404)
    return jsonify({'tarea': tarea})

# CORRECCIÓN: Manejador de error 404 añadido al código completo
@app.errorhandler(404)
def no_encontrado(error):
    return make_response(jsonify({'error': 'Tarea inexistente'}), 404)