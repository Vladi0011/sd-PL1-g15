from flask import Flask, jsonify, abort

app = Flask(__name__)

# CORRECCIÓN: Cambio de 'titulo' a 'descripcion' para coherencia
tareas = [
    {"id": 1, "descripcion": "Estudiar Flask", "completada": False},
    {"id": 2, "descripcion": "Hacer práctica de SD", "completada": True}
]

def buscar_tarea(id):
    for t in tareas:
        if t['id'] == id:
            return t
    return None

@app.route('/lista/v1/tarea/<int:id>', methods=["GET"])
def get_tarea(id):
    tarea = buscar_tarea(id)
    # En el ejercicio 1 aun no se usaba abort, se devolvía JSON manual
    if tarea:
        return jsonify({'tarea': tarea})
    else:
        return jsonify({'error': 'Tarea no encontrada'}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)