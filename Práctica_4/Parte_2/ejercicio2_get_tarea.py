from flask import Flask, jsonify, abort

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

@app.route('/lista/v1/tarea/<int:id>', methods=["GET"])
def get_tarea(id):
    tarea = buscar_tarea(id)
    if tarea is None:
        abort(404) # CORRECCIÓN: Uso correcto de abort
    return jsonify({'tarea': tarea})