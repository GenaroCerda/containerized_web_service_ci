import os

import psycopg2
import redis
from flask import Flask, jsonify

app = Flask(__name__) # Inicializa la instancia de la aplicacion web en Flask

def get_db():
    return psycopg2.connect(
        host=os.environ["DB_HOST"],
        dbname=os.environ["POSTGRES_DB"],
        user=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
        connect_timeout=3,
    )

def get_redis():
    return redis.Redis(host=os.environ["REDIS_HOST"], port=6379, decode_responses=True)


@app.get("/health") # Decorador que se encarga de la logica de un GET
def health():
    return jsonify(status="ok")

@app.get("/")
def index():
    return jsonify(message="Hola desde mi API")

@app.get("/ready")
def ready():
    # Readiness: "puedo atender tráfico", verifica dependencias.
    try:
        with get_db() as conn, conn.cursor() as cur:
            cur.execute("SELECT 1")
        get_redis().ping()
    except Exception as exc:
        return jsonify(status="not ready", error=str(exc)), 503
    return jsonify(status="ready")


@app.get("/visits")
def visits():
    count = get_redis().incr("visits")
    return jsonify(visits=count)


@app.get("/db-time")
def db_time():
    with get_db() as conn, conn.cursor() as cur:
        cur.execute("SELECT now()")
        return jsonify(db_time=str(cur.fetchone()[0]))