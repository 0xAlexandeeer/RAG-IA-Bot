
from pathlib import Path
from docx import Document
from docx.text.paragraph import Paragraph
from docx.table import Table

# 1. Definir ubicación
carpeta = Path(__file__).resolve().parent

archivo = (
    carpeta
    / "documentos"
    / "finanzas"
    / "catalogo_clases_subclases.docx"
)

# 2. Abrir el Word
documento = Document(archivo)

print("LECTOR DE DOCUMENTOS WORD")
print(f"Archivo: {archivo.name}")

# 3. Recorrer los elementos en orden
for elemento in documento.iter_inner_content():

    if isinstance(elemento, Paragraph):

        texto = elemento.text.strip()

        if texto:
            print(f"\nPÁRRAFO: {texto}")
            print(f"Estilo: {elemento.style.name}")

    elif isinstance(elemento, Table):

        print("\nTABLA ENCONTRADA")

        for fila in elemento.rows:

            valores = [
                celda.text.strip()
                for celda in fila.cells
            ]

            print(valores)
