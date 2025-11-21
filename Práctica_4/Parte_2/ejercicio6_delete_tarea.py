@app.route('/lista/v1/tarea/<int:id>', methods=["DELETE"])
def delete_tarea(id):
    tarea = buscar_tarea(id)
    if tarea is None:
        abort(404)
    tareas.remove(tarea)
    return jsonify({'borrado': True})
