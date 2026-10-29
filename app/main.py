import os

import psycopg2
import redis
from flask import Flask, jsonify, request

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
    except Exception as exc: # noqa: BLE001
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

@app.post("/notes")
def add_note():
    text = (request.get_json(silent=True) or {}).get("text", "")
    if not text:
        return jsonify(error="falta 'text'"), 400
    with get_db() as conn, conn.cursor() as cur:
        cur.execute(
            "CREATE TABLE IF NOT EXISTS notes ("
            "id SERIAL PRIMARY KEY, text TEXT NOT NULL, created_at TIMESTAMPTZ DEFAULT now())"
        )
        cur.execute("INSERT INTO notes (text) VALUES (%s) RETURNING id", (text,))
        return jsonify(id=cur.fetchone()[0]), 201


@app.get("/notes")
def list_notes():
    with get_db() as conn, conn.cursor() as cur:
        cur.execute(
            "CREATE TABLE IF NOT EXISTS notes ("
            "id SERIAL PRIMARY KEY, text TEXT NOT NULL, created_at TIMESTAMPTZ DEFAULT now())"
        )
        cur.execute("SELECT id, text, created_at FROM notes ORDER BY id")
        return jsonify([{"id": r[0], "text": r[1], "created_at": str(r[2])} for r in cur.fetchall()])