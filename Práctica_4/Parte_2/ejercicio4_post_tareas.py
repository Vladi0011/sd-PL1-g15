@app.route("/lista/v1/tareas", methods=["POST"])
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

@app.errorhandler(400)
def solicitud_invalida(error):
    return make_response(jsonify({'error': 'Solicitud incorrecta'}), 400)
