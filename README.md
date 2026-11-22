# AI Bot - RAG Corporativo

AI Bot es un asistente conversacional basado en RAG (Retrieval-Augmented Generation) que consulta documentos internos y responde preguntas con información respaldada por fuentes corporativas.

El proyecto utiliza Gemini para generar embeddings y respuestas, SQLite para almacenar chunks y vectores, y similitud coseno para recuperar la evidencia más relevante.

## Características

- Segmentación estructurada de documentos por secciones
- Generación incremental de embeddings con Gemini
- Almacenamiento persistente en SQLite
- Recuperación semántica mediante similitud coseno
- Respuestas limitadas a la información recuperada
- Identificación de las fuentes y secciones utilizadas
- Evaluación básica de recuperación con Recall@K y MRR

## Arquitectura

```text
Documento
   |
   v
Ingesta -> chunks.json -> SQLite (chunks)
                              |
                              v
                       Embeddings (Gemini)
                              |
                              v
                    SQLite (embeddings/vectores)
                              |
                              v
Pregunta -> Embedding -> Similitud coseno -> Evidencia
                                                    |
                                                    v
                                            Respuesta Gemini
```

## Tecnologías

- Python 3
- Google Gemini API
- SQLite
- python-dotenv

## Estructura del proyecto

```text
.
|-- README.md
|-- requirements.txt
|-- .env.example
|-- bot_gemini.py
|-- memoria.db
`-- rag_corporativo/
    |-- documentos/
    |-- catalogo.json
    |-- ingesta.py
    |-- indexador.py
    |-- embeddings.py
    |-- buscador.py
    |-- generador.py
    `-- evaluacion.py
```

## Requisitos

- Python 3.10 o superior
- Una API key de Google Gemini

## Instalación

1. Clona el repositorio:

```bash
git clone https://github.com/0xAlexandeeer/RAG-IA-Bot.git
cd RAG-IA-Bot
```

2. Crea y activa un entorno virtual:

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

Linux o macOS:

```bash
source .venv/bin/activate
```

3. Instala las dependencias:

```bash
pip install -r requirements.txt
```

4. Configura tu API key:

```bash
copy .env.example .env
```

Abre `.env` y reemplaza el valor de `GEMINI_API_KEY`.

## Uso

Ejecuta los módulos en este orden:

```bash
python rag_corporativo/ingesta.py
python rag_corporativo/indexador.py
python rag_corporativo/embeddings.py
python rag_corporativo/generador.py
```

Dentro del chatbot, escribe `salir` para finalizar la sesión.

Para ejecutar el buscador sin generar respuestas, utiliza:

```bash
python rag_corporativo/buscador.py
```

Para revisar la evaluación básica de recuperación:

```bash
python rag_corporativo/evaluacion.py
```

## Formato de documentos

Los documentos deben colocarse en `rag_corporativo/documentos/` y su metadata debe registrarse en `rag_corporativo/catalogo.json`.

El proceso de ingesta organiza el contenido en chunks. Cada chunk conserva su identificación, versión, estado, vigencia y sección de origen.

## Seguridad

No subas tu archivo `.env` ni compartas tu API key. Los archivos `.env` y las bases de datos locales están excluidos mediante `.gitignore`.

## Autor

Desarrollado por 0xAlexandeeer.

## Licencia

Este proyecto no incluye una licencia definida. Agrega una licencia antes de distribuirlo públicamente si deseas establecer condiciones de uso.
