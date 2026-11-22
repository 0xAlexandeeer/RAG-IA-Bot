
from pathlib import Path
import re
import json

# 1. Definir rutas
carpeta = Path(__file__).resolve().parent

archivo = carpeta / "documentos" / "politica_presupuestos.txt"
catalogo = carpeta / "catalogo.json"

# 2. Leer documento y metadata
texto = archivo.read_text(encoding="utf-8").strip()

metadata = json.loads(
    catalogo.read_text(encoding="utf-8")
)

if not texto:
    raise ValueError("El documento está vacío.")

# 3. Dividir el documento por secciones
partes = re.split(
    r"(?=^\d+\.\s)",
    texto,
    flags=re.MULTILINE
)

cabecera = partes[0].strip()

fragmentos = [
    p.strip() for p in partes[1:] if p.strip()
]

# 4. Crear chunks estructurados
chunks = []
## Aca crea los loops para crear los chunks, cada chunk es un diccionario con la metadata y el contenido de la sección
for numero, fragmento in enumerate(fragmentos, 1):

    # Obtener el título de la sección
    seccion = fragmento.split("\n")[0]

    # Construir un registro con metadata
    chunk = {
        "documento_id": metadata["documento_id"],
        "version": metadata["version"],
        "estado": metadata["estado"],
        "vigente_desde": metadata["vigente_desde"],
        "archivo": metadata["archivo"],
        "chunk_id": numero,
        "seccion": seccion,
        "contenido": fragmento
    }

    chunks.append(chunk)

# 5. Guardar resultado estructurado
salida = carpeta / "chunks.json"

salida.write_text(
    json.dumps(chunks, indent=4, ensure_ascii=False),
    encoding="utf-8"
)

print(f"Documento: {metadata['titulo']}")
print(f"Versión: {metadata['version']}")
print(f"Estado: {metadata['estado']}")
print(f"Chunks generados: {len(chunks)}")
print("Metadata guardada correctamente.")
