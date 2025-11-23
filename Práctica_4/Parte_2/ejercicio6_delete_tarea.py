from flask import Flask, jsonify, request, abort, make_response

app = Flask(__name__)

tareas = [
    {'id': 1, 'descripcion': 'Tarea 1', 'completada': True},
    {'id': 2, 'descripcion': 'Tarea 2', 'completada': False}
]

def buscar_tarea(id):
    for t in tareas:
        if t['id'] == id:
            return t
    return None

# ... (Se omiten GET, POST y PUT por brevedad, pero irían aquí) ...

# CORRECCIÓN: Implementación completa de DELETE
@app.route('/lista/v1/tarea/<int:id>', methods=["DELETE"])
def delete_tarea(id):
    tarea = buscar_tarea(id)
    if tarea is None:
        abort(404)
    tareas.remove(tarea)
    return jsonify({'borrado': True})

@app.errorhandler(404)
def no_encontrado(error):
    return make_response(jsonify({'error': 'Tarea inexistente'}), 404)