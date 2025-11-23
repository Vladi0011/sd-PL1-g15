from flask import Flask, jsonify, abort, make_response, request

app = Flask(__name__)

tareas = [
    {'id': 1, 'descripcion': 'Tarea 1', 'completada': True}
]

# ... (Aquí irían las rutas GET y buscar_tarea igual que en el anterior) ...
# Para ahorrar espacio, pongo directamente la parte del experimento:

@app.route("/lista/v1/tareas", methods=["GET"])
def get_tareas():
    return jsonify({"tareas": tareas})

# --- PARTE DEL EXPERIMENTO 4 ---
@app.route("/lista/v1/tareas", methods=["POST"])
def create_tarea():
    print("Diccionario JSON recibido:")
    print(request.json)  # Imprimimos el objeto Python ya convertido
    print("-------")
    # Verificamos tipos de datos
    if request.json:
        if 'completada' in request.json:
            print(f"Tipo de 'completada': {type(request.json['completada'])}")
    return "OK", 201
# -------------------------------

if __name__ == "__main__":
    app.run(debug=True)