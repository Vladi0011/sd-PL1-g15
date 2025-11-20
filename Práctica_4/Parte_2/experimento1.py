# coding: utf-8
from flask import Flask, jsonify

app = Flask(__name__)
tareas = []  # Inicialmente vacía

@app.route("/lista/v1/tareas", methods=["GET"])
def get_tareas():
    return jsonify({"tareas": tareas})
