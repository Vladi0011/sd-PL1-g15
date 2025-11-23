from flask import Flask, jsonify, request, abort, make_response

app = Flask(__name__)

# Lista inicial de tareas
tareas = [
    {'id': 1, 'descripcion': 'Terminar práctica Hola Mundo con Flask', 'completada': True},
    {'id': 2, 'descripcion': 'Terminar práctica aplicación To-Do', 'completada': False}
]

# Función para buscar tarea por ID
def buscar_tarea(id):
    for t in tareas:
        if t['id'] == id:
            return t
    return None

# Ruta para actualizar una tarea existente
@app.route('/lista/v1/tarea/<int:id>', methods=["PUT"])
def update_tarea(id):
    tarea = buscar_tarea(id)
    if tarea is None:
        abort(404)

    if not request.json:
        abort(400)

    if 'descripcion' in request.json:
        if type(request.json['descripcion']) != str:
            abort(400)
        tarea['descripcion'] = request.json['descripcion']

    if 'completada' in request.json:
        if type(request.json['completada']) != bool:
            abort(400)
        tarea['completada'] = request.json['completada']

    return jsonify(tarea)

# Manejadores de error
@app.errorhandler(404)
def no_encontrado(error):
    return make_response(jsonify({'error': 'Tarea inexistente'}), 404)

@app.errorhandler(400)
def solicitud_invalida(error):
    return make_response(jsonify({'error': 'Solicitud incorrecta'}), 400)
