from flask import Flask, jsonify

app = Flask(__name__)

# Lista de tareas de ejemplo
tareas = [
    {"id": 1, "titulo": "Estudiar Flask"},
    {"id": 2, "titulo": "Hacer práctica de SD"},
    {"id": 3, "titulo": "Preparar presentación"}
]

@app.route('/lista/v1/tarea/<int:id>', methods=["GET"])
def get_tarea(id):
    tarea = buscar_tarea(id)
    if tarea:
        return jsonify({'tarea': tarea})
    else:
        return jsonify({'error': 'Tarea no encontrada'}), 404

def buscar_tarea(id):
    for t in tareas:
        if t['id'] == id:
            return t
    return None

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
