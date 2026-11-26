
from pathlib import Path

# Carpeta raíz del proyecto
carpeta = Path(__file__).resolve().parent

# Repositorio documental
repositorio = carpeta / "documentos" / "finanzas"

# Formatos que queremos identificar
formatos = {".txt", ".pdf", ".docx", ".xlsx"}

archivos = [
    archivo
    for archivo in repositorio.rglob("*")
    if archivo.is_file()
    and archivo.suffix.lower() in formatos
]

print(f"Documentos encontrados: {len(archivos)}")

for archivo in archivos:
    print(f"Documento: {archivo.name}")
    print(f"Formato: {archivo.suffix.lower()}")
    print(f"Ruta relativa: {archivo.relative_to(repositorio)}")
    print("-" * 40)
