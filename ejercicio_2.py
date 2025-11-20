from flask import Flask, jsonify, request, abort, make_response, url_for

app = Flask(__name__)

# Lista inicial de tareas
tareas = [
    {'id': 1, 'descripcion': 'Terminar práctica Hola Mundo con Flask', 'completada': True},
    {'id': 2, 'descripcion': 'Terminar práctica aplicación To-Do', 'completada': False}
]

 #Funcion nueva del ejercicio 
def generar_nuevo_id():
    if not tareas:              # si la lista está vacía
        return 1
    # si hay tareas, usamos el máximo id existente + 1
    return max(t['id'] for t in tareas) + 1

# Función para buscar tarea por ID
def buscar_tarea(id):
    for t in tareas:
        if t['id'] == id:
            return t
    return None

# Función para convertir tarea a formato HATEOAS
def hacer_publica(tarea):
    nueva = {}
    for campo in tarea:
        if campo == 'id':
            nueva['uri'] = url_for('get_tarea', id=tarea['id'], _external=True)
        else:
            nueva[campo] = tarea[campo]
    return nueva

# GET lista completa
@app.route('/lista/v1/tareas', methods=["GET"])
def get_tareas():
    return jsonify({'tareas': [hacer_publica(t) for t in tareas]})

# GET tarea específica
@app.route('/lista/v1/tarea/<int:id>', methods=["GET"])
def get_tarea(id):
    tarea = buscar_tarea(id)
    if tarea is None:
        abort(404)
    return jsonify({'tarea': hacer_publica(tarea)})

# POST nueva tarea
@app.route('/lista/v1/tareas', methods=["POST"])
def create_tarea():
    if not request.json or 'descripcion' not in request.json:
        abort(400)

    nueva = {
        'id': generar_nuevo_id(),   # <-- usamos la función nueva
        'descripcion': request.json['descripcion'],
        'completada': request.json.get('completada', False)
    }
    tareas.append(nueva)
    return jsonify(hacer_publica(nueva)), 201

# PUT actualizar tarea
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
    return jsonify(hacer_publica(tarea))

# DELETE eliminar tarea
@app.route('/lista/v1/tarea/<int:id>', methods=["DELETE"])
def delete_tarea(id):
    tarea = buscar_tarea(id)
    if tarea is None:
        abort(404)
    tareas.remove(tarea)
    return jsonify({'borrado': True})

# Manejadores de error
@app.errorhandler(404)
def no_encontrado(error):
    return make_response(jsonify({'error': 'Tarea inexistente'}), 404)

@app.errorhandler(400)
def solicitud_invalida(error):
    return make_response(jsonify({'error': 'Solicitud incorrecta'}), 400)
# permitir CORS 
@app.after_request
def after(response):
    # Permitir acceso desde cualquier origen (el comapñero, tú, etc.)
    response.headers.add('Access-Control-Allow-Origin', '*')
    # Cabeceras que permitimos que nos envíen
    response.headers.add('Access-Control-Allow-Headers', 'content-type, authorization')
    # Métodos HTTP permitidos
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')
    return response
