from pathlib import Path
from docx import Document as WordDocument
from langchain_core.documents import Document

# 1. Ruta del archivo
carpeta = Path(__file__).resolve().parent

archivo = (
    carpeta / "documentos" / "finanzas"
    / "catalogo_clases_subclases.docx"
)

# 2. Leer el Word con python-docx
word = WordDocument(archivo)

# 3. Preparar documentos LangChain
documentos = []

for tabla in word.tables:

    # Omitir fila de encabezados
    for numero, fila in enumerate(tabla.rows[1:], start=2):

        valores = [
            celda.text.strip()
            for celda in fila.cells
        ]

        codigo, clase, subclase = valores

        documento = Document(
            page_content=(
                f"Código: {codigo}\n"
                f"Clase: {clase}\n"
                f"Subclase: {subclase}"
            ),
            metadata={
                "source": archivo.name,
                "fila": numero,
                "codigo": codigo,
                "clase": clase,
                "subclase": subclase
            }
        )

        documentos.append(documento)

print(f"Documentos LangChain: {len(documentos)}")

# 4. Inspeccionar un código específico
for documento in documentos:
    if documento.metadata["codigo"] == "6399000035":
        print("\nCONTENIDO:")
        print(documento.page_content)

        print("\nMETADATA:")
        print(documento.metadata)
        break