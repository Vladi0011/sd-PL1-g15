from flask import Flask, jsonify, request, abort, make_response

app = Flask(__name__)

tareas = [
    {'id': 1, 'descripcion': 'Tarea Inicial', 'completada': False}
]

def buscar_tarea(id):
    for t in tareas:
        if t['id'] == id:
            return t
    return None

@app.route('/lista/v1/tareas', methods=["GET"])
def get_tareas():
    return jsonify({'tareas': tareas})

@app.route('/lista/v1/tareas', methods=["POST"])
def create_tarea():
    if not request.json or 'descripcion' not in request.json:
        abort(400)
    nueva = {
        'id': tareas[-1]['id'] + 1 if tareas else 1,
        'descripcion': request.json['descripcion'],
        'completada': request.json.get('completada', False)
    }
    tareas.append(nueva)
    return jsonify(nueva), 201

@app.route('/lista/v1/tarea/<int:id>', methods=["DELETE"])
def delete_tarea(id):
    tarea = buscar_tarea(id)
    if tarea is None:
        abort(404)
    tareas.remove(tarea)
    return jsonify({'borrado': True})

# (Se omiten PUT y GET individual por brevedad, pero no afectan a este test)