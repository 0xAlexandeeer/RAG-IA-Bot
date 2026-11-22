
# Clase 8: Evaluación de Retrieval

# 1. Dataset de evaluación
casos = [
    {
        "pregunta": "¿Quién aprueba una ampliación?",
        "relevante": "3. APROBACIONES",
        "ranking": [
            "3. APROBACIONES",
            "1. OBJETIVO",
            "4. SEGUIMIENTO",
            "2. SOLICITUDES"
        ]
    },
    {
        "pregunta": "¿Por dónde ingreso mi solicitud?",
        "relevante": "2. SOLICITUDES",
        "ranking": [
            "1. OBJETIVO",
            "4. SEGUIMIENTO",
            "3. APROBACIONES",
            "2. SOLICITUDES"
        ]
    }
]


# 2. Evaluar distintos valores de K
def evaluar(casos, k):

    aciertos = 0
    suma_rr = 0

    for caso in casos:

        resultados = caso["ranking"][:k]
        esperado = caso["relevante"]

        if esperado in resultados:

            aciertos += 1

            posicion = resultados.index(esperado) + 1

            suma_rr += 1 / posicion

    total = len(casos)

    recall = aciertos / total
    mrr = suma_rr / total

    return recall, mrr


# 3. Ejecutar evaluación
for k in [3, 4]:

    recall, mrr = evaluar(casos, k)

    print(f"\nEVALUACIÓN TOP-{k}")
    print(f"Recall@{k}: {recall:.2%}")
    print(f"MRR@{k}: {mrr:.4f}")
