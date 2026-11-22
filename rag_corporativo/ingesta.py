
from pathlib import Path
import re
import json

carpeta = Path(__file__).resolve().parent

archivo = carpeta / "documentos" / "politica_presupuestos.txt"
catalogo = carpeta / "catalogo.json"

texto = archivo.read_text(encoding="utf-8").strip()

metadata = json.loads(
    catalogo.read_text(encoding="utf-8")
)

if not texto:
    raise ValueError("El documento está vacío.")

partes = re.split(
    r"(?=^\d+\.\s)",
    texto,
    flags=re.MULTILINE
)

cabecera = partes[0].strip()

fragmentos = [
    p.strip() for p in partes[1:] if p.strip()
]

chunks = []
for numero, fragmento in enumerate(fragmentos, 1):
    seccion = fragmento.split("\n")[0]
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
