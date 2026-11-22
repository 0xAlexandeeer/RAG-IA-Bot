
from pathlib import Path
import sqlite3
import json

carpeta = Path(__file__).resolve().parent

archivo_json = carpeta / "chunks.json"
archivo_db = carpeta / "rag.db"

chunks = json.loads(
    archivo_json.read_text(encoding="utf-8")
)

conexion = sqlite3.connect(archivo_db)

conexion.execute("""
    CREATE TABLE IF NOT EXISTS chunks (
        documento_id TEXT NOT NULL,
        version TEXT NOT NULL,
        chunk_id INTEGER NOT NULL,
        estado TEXT,
        vigente_desde TEXT,
        archivo TEXT,
        seccion TEXT,
        contenido TEXT NOT NULL,
        PRIMARY KEY (documento_id, version, chunk_id)
    )
""")

for chunk in chunks:
    conexion.execute("""
        INSERT INTO chunks (
            documento_id,
            version,
            chunk_id,
            estado,
            vigente_desde,
            archivo,
            seccion,
            contenido
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(documento_id, version, chunk_id)
        DO UPDATE SET
            estado = excluded.estado,
            vigente_desde = excluded.vigente_desde,
            archivo = excluded.archivo,
            seccion = excluded.seccion,
            contenido = excluded.contenido
    """, (
        chunk["documento_id"],
        chunk["version"],
        chunk["chunk_id"],
        chunk["estado"],
        chunk["vigente_desde"],
        chunk["archivo"],
        chunk["seccion"],
        chunk["contenido"]
    ))

conexion.commit()

resultados = conexion.execute("""
    SELECT documento_id, version, chunk_id, seccion
    FROM chunks
    ORDER BY version, chunk_id
""").fetchall()

print(f"Registros almacenados: {len(resultados)}")

for fila in resultados:
    print(fila)

conexion.close()
