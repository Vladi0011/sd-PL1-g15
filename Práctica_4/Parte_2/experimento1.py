from flask import Flask, jsonify

app = Flask(__name__)

tareas = [
    {'id': 1, 'descripcion': 'Terminar práctica Hola Mundo con Flask', 'completada': True},
    {'id': 2, 'descripcion': 'Terminar práctica aplicación To-Do', 'completada': False}
]

@app.route("/lista/v1/tareas", methods=["GET"])
def get_tareas():
    return jsonify({"tareas": tareas})

# Nota: Para ejecutar, usar gunicorn o añadir if __name__ == "__main__": app.run()