from flask import Flask, jsonify

app = Flask(__name__) # Inicializa la instancia de la aplicacion web en Flask

@app.get("/cannabis") # Decorador que se encarga de la logica de un GET
def health():
    return jsonify(status="ok")

@app.get("/")
def index():
    return jsonify(message="Hola desde mi API")