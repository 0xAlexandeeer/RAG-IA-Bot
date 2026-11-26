
from pathlib import Path

# 1. Definir nuestro repositorio
carpeta = Path(__file__).resolve().parent
repositorio = carpeta / "documentos"

# 2. Identificar archivos TXT
archivos = sorted(repositorio.rglob("*.txt"))

print("LECTOR DOCUMENTAL CORPORATIVO")
print(f"Archivos detectados: {len(archivos)}")

# 3. Leer cada documento
for archivo in archivos:

    print("\n--------------------------")
    print(f"Documento: {archivo.name}")

    # Obtener la ubicación dentro del repositorio
    ruta_relativa = archivo.relative_to(repositorio)

    print(f"Ruta: {ruta_relativa}")

    # Leer el contenido del documento
    texto = archivo.read_text(
        encoding="utf-8-sig"
    ).strip()

    # 4. Validar el contenido
    if not texto:
        print("Estado: DOCUMENTO VACÍO")
        continue

    print("Estado: DOCUMENTO VÁLIDO")
    print(f"Caracteres: {len(texto)}")

    # 5. Mostrar las primeras líneas
    lineas = texto.splitlines()

    print("Vista previa:")

    for linea in lineas[:5]:
        print(linea)
