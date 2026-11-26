
from pathlib import Path
import json
import re

# 1. Configuración
carpeta = Path(__file__).resolve().parent
repositorio = carpeta / "documentos"

ruta_catalogo = carpeta / "catalogo_documentos.json"

# 2. Leer catálogo
catalogo = json.loads(
    ruta_catalogo.read_text(encoding="utf-8")
)

chunks_totales = []
identidades = set()

# 3. Recorrer los documentos del catálogo
for documento in catalogo:

    doc_id = documento["documento_id"]
    version = documento["version"]

    # Validar identidad documental
    identidad = (doc_id, version)

    if identidad in identidades:
        raise ValueError(
            f"Documento y versión duplicados: {identidad}"
        )

    identidades.add(identidad)

    # Construir ruta del documento
    archivo = repositorio / documento["ruta"]

    if not archivo.is_file():
        raise FileNotFoundError(archivo)

    # 4. Leer contenido
    texto = archivo.read_text(
        encoding="utf-8-sig"
    ).strip()

    if not texto:
        raise ValueError(
            f"Documento vacío: {archivo.name}"
        )

    # 5. Fragmentar por secciones numeradas
    partes = re.split(
        r"(?=^\d+\.\s)",
        texto,
        flags=re.MULTILINE
    )

    cabecera = partes[0].strip()
    titulo = cabecera.splitlines()[0]

    fragmentos = [
        parte.strip()
        for parte in partes[1:]
        if parte.strip()
    ]

    if not fragmentos:
        raise ValueError(
            f"No se encontraron secciones en {archivo.name}"
        )

    # 6. Crear chunks con metadata
    for numero, fragmento in enumerate(fragmentos, 1):

        seccion = fragmento.splitlines()[0]

        chunk = {
            "documento_id": doc_id,
            "version": version,
            "estado": documento["estado"],
            "area": documento["area"],
            "archivo": documento["ruta"],
            "titulo": titulo,
            "vigente_desde": documento.get("vigente_desde"),
            "chunk_id": numero,
            "seccion": seccion,
            "contenido": fragmento
        }

        chunks_totales.append(chunk)

    print(
        f"{archivo.name}: {len(fragmentos)} chunks"
    )

# 7. Guardar el resultado
salida = carpeta / "chunks_multi.json"

salida.write_text(
    json.dumps(
        chunks_totales,
        indent=4,
        ensure_ascii=False
    ),
    encoding="utf-8"
)

print("--------------------------")
print(f"Documentos: {len(catalogo)}")
print(f"Chunks totales: {len(chunks_totales)}")
print("Ingesta finalizada.")
