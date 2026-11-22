
from pathlib import Path
import sqlite3
import json
import math
import hashlib
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

carpeta = Path(__file__).resolve().parent
load_dotenv(carpeta.parent / ".env")

MODELO = "gemini-embedding-001"
DIMENSIONES = 768

cliente = genai.Client(
    api_key=os.environ["GEMINI_API_KEY"]
)

def similitud_coseno(a, b):

    if len(a) != len(b):
        raise ValueError("Dimensiones incompatibles")

    producto = sum(x * y for x, y in zip(a, b))

    norma_a = math.sqrt(sum(x*x for x in a))
    norma_b = math.sqrt(sum(y*y for y in b))

    if norma_a == 0 or norma_b == 0:
        return 0.0

    return producto / (norma_a * norma_b)


def cargar_documentos():

    with sqlite3.connect(carpeta / "rag.db") as conexion:

        registros = conexion.execute("""
            SELECT
                c.documento_id,
                c.version,
                c.chunk_id,
                c.seccion,
                c.contenido,
                e.vector,
                e.huella
            FROM chunks c
            JOIN embeddings e
              ON c.documento_id = e.documento_id
             AND c.version = e.version
             AND c.chunk_id = e.chunk_id
            WHERE c.estado = 'vigente'
              AND e.modelo = ?
              AND e.dimensiones = ?
        """, (MODELO, DIMENSIONES)).fetchall()

    documentos = []

    for doc_id, version, chunk_id, seccion, contenido, vector, huella in registros:

        texto = f"{seccion}\n{contenido}"

        huella_actual = hashlib.sha256(
            texto.encode("utf-8")
        ).hexdigest()

        if huella_actual != huella:
            print(f"Chunk {chunk_id}: requiere reindexación")
            continue

        documentos.append({
            "documento_id": doc_id,
            "version": version,
            "chunk_id": chunk_id,
            "seccion": seccion,
            "contenido": contenido,
            "vector": json.loads(vector)
        })

    return documentos


def vectorizar_pregunta(pregunta):

    respuesta = cliente.models.embed_content(
        model=MODELO,
        contents=pregunta,
        config=types.EmbedContentConfig(
            task_type="RETRIEVAL_QUERY",
            output_dimensionality=DIMENSIONES
        )
    )

    return respuesta.embeddings[0].values


def buscar(pregunta, documentos):

    vector_pregunta = vectorizar_pregunta(pregunta)

    resultados = []

    for documento in documentos:

        puntuacion = similitud_coseno(
            vector_pregunta,
            documento["vector"]
        )

        resultados.append((puntuacion, documento))

    resultados.sort(
        key=lambda resultado: resultado[0],
        reverse=True
    )

    return resultados[:4]



def main():

    documentos = cargar_documentos()

    if not documentos:
        raise RuntimeError("No hay documentos indexados vigentes")

    print("BUSCADOR DOCUMENTAL CORPORATIVO")
    print(f"Chunks disponibles: {len(documentos)}")

    while True:

        pregunta = input("\nPregunta: ").strip()

        if pregunta.lower() == "salir":
            break

        if not pregunta:
            continue

        resultados = buscar(pregunta, documentos)

        for puntuacion, documento in resultados:

            print("\n----------------------------")
            print(f"Similitud: {puntuacion:.4f}")
            print(f"Documento: {documento['documento_id']}")
            print(f"Versión: {documento['version']}")
            print(f"Sección: {documento['seccion']}")
            print(f"Contenido: {documento['contenido']}")


if __name__ == "__main__":
    main()
