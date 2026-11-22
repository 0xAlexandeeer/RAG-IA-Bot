
from pathlib import Path
import sqlite3
import json
import hashlib
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

carpeta = Path(__file__).resolve().parent

load_dotenv(carpeta.parent / ".env")

MODELO = "gemini-embedding-001"
DIMENSIONES = 768

conexion = sqlite3.connect(carpeta / "rag.db")
conexion.execute("PRAGMA foreign_keys = ON")

conexion.execute("""
    CREATE TABLE IF NOT EXISTS embeddings (
        documento_id TEXT NOT NULL,
        version TEXT NOT NULL,
        chunk_id INTEGER NOT NULL,
        modelo TEXT NOT NULL,
        dimensiones INTEGER NOT NULL,
        huella TEXT NOT NULL,
        vector TEXT NOT NULL,

        PRIMARY KEY (
            documento_id, version,
            chunk_id, modelo, dimensiones
        ),

        FOREIGN KEY (documento_id, version, chunk_id)
        REFERENCES chunks(documento_id, version, chunk_id)
    )
""")

chunks = conexion.execute("""
    SELECT documento_id, version, chunk_id,
           seccion, contenido
    FROM chunks
    WHERE estado = 'vigente'
    ORDER BY documento_id, version, chunk_id
""").fetchall()

pendientes = []

for doc_id, version, chunk_id, seccion, contenido in chunks:

    texto = f"{seccion}\n{contenido}"

    huella = hashlib.sha256(
        texto.encode("utf-8")
    ).hexdigest()

    existente = conexion.execute("""
        SELECT huella FROM embeddings
        WHERE documento_id = ?
          AND version = ?
          AND chunk_id = ?
          AND modelo = ?
          AND dimensiones = ?
    """, (doc_id, version, chunk_id, MODELO, DIMENSIONES)).fetchone()

    if existente is None or existente[0] != huella:
        pendientes.append(
            (doc_id, version, chunk_id, texto, huella)
        )

print(f"Chunks pendientes: {len(pendientes)}")

if pendientes:

    cliente = genai.Client(
        api_key=os.environ["GEMINI_API_KEY"]
    )

    respuesta = cliente.models.embed_content(
        model=MODELO,
        contents=[item[3] for item in pendientes],
        config=types.EmbedContentConfig(
            task_type="RETRIEVAL_DOCUMENT",
            output_dimensionality=DIMENSIONES
        )
    )

    if len(respuesta.embeddings) != len(pendientes):
        raise RuntimeError("Cantidad inesperada de embeddings")

    with conexion:
        for item, embedding in zip(
            pendientes, respuesta.embeddings
        ):
            doc_id, version, chunk_id, texto, huella = item

            vector = embedding.values

            if len(vector) != DIMENSIONES:
                raise ValueError("Dimensiones incorrectas")

            conexion.execute("""
                INSERT INTO embeddings
                VALUES (?, ?, ?, ?, ?, ?, ?)

                ON CONFLICT(
                    documento_id, version,
                    chunk_id, modelo, dimensiones
                )
                DO UPDATE SET
                    huella = excluded.huella,
                    vector = excluded.vector
            """, (
                doc_id, version, chunk_id,
                MODELO, DIMENSIONES,
                huella, json.dumps(vector)
            ))

total = conexion.execute(
    "SELECT COUNT(*) FROM embeddings"
).fetchone()[0]

print(f"Embeddings almacenados: {total}")
print("Proceso finalizado.")

conexion.close()
