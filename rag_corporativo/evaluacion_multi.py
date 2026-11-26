
from buscador import cargar_documentos, buscar

# 1. Definir casos de evaluación
casos = [
    {
        "pregunta": (
            "¿Cómo se calcula el margen bruto? "
            "Dame la fórmula y un ejemplo."
        ),
        "relevantes": {
            ("PROC-MARG-001", 3),
            ("PROC-MARG-001", 4),
            ("GLOS-FIN-001", 4)
        }
    },
    {
        "pregunta": "¿Qué significa EBITDA?",
        "relevantes": {
            ("GLOS-FIN-001", 5)
        }
    },
    {
        "pregunta": (
            "¿Quién debe aprobar una ampliación "
            "presupuestal superior a S/ 1,000?"
        ),
        "relevantes": {
            ("POL-PRES-001", 3)
        }
    }
]

# 2. Recuperar documentos indexados
documentos = cargar_documentos()

# 3. Evaluar con distintos valores de K
for caso in casos:

    print("\n--------------------------")
    print(f"Pregunta: {caso['pregunta']}")

    resultados = buscar(
        caso["pregunta"],
        documentos
    )

    # Identificadores recuperados en orden
    ranking = [
        (
            documento["documento_id"],
            documento["chunk_id"]
        )
        for puntuacion, documento in resultados
    ]

    esperados = caso["relevantes"]

    # 4. Calcular Recall@K
    for k in [1, 2, 4]:

        recuperados = set(ranking[:k])

        aciertos = recuperados.intersection(
            esperados
        )

        recall = len(aciertos) / len(esperados)

        print(
            f"Recall@{k}: {recall:.2%}"
        )
