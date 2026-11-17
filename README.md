# Extractor de Tareas con NLP (spaCy)

Un script de Inteligencia Artificial en Python que analiza notas de texto en lenguaje natural y extrae la información clave estructurándola en formato JSON. Ideal para automatizar la recolección de eventos o tareas diarias.

## ¿Qué hace?
Utiliza Procesamiento de Lenguaje Natural (NLP) mediante la librería **spaCy** para:
- Detectar y extraer los **verbos/acciones principales** de una frase (ej. "comprar", "ir", "tener").
- Aplicar un sistema de reglas estrictas (`Matcher`) para cazar con precisión:
  - **Días de la semana** (lunes, martes...)
  - **Horas** en formato numérico (10:00, 20:30...)
  - **Momentos del día** (mañana, tarde, noche...)
- Exportar automáticamente los datos extraídos a un archivo `tarea_estructurada.json`.

## Cómo usarlo

1. Activa tu entorno virtual (`uv venv`).
2. Asegúrate de tener instalado spaCy y el modelo en español:
   ```bash
   pip install spacy
   python -m spacy download es_core_news_sm
   ```
3. Modifica la variable `nota` dentro de `main.py` con el texto que quieras analizar
4. Ejecuta el script:
    ```bash
    python main.py
    ```

## Tecnologías utilizadas
- Python 3
- SpaCy (Modelo de lenguaje: `es_core_news_sm` + `Matcher`)
- Librería nativa `json`