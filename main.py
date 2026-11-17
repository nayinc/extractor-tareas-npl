import spacy
from spacy.matcher import Matcher
import json

print("Cargando modelo de IA...")
npl = spacy.load("es_core_news_sm")

# diccionario de palabras clave
tarea_estructurada = {
    "acciones": [],
    "dias": [],
    "horas": []
}

matcher = Matcher(npl.vocab)

# reglas dias
dias = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
patron_dia = [{"LOWER": {"IN": dias}}]
matcher.add("DIA", [patron_dia])

# reglas horas
patron_hora = [{"SHAPE": "dd:dd"}]
matcher.add("HORA", [patron_hora])

nota = "El miércoles tengo turno a las 20:30 y el viernes tengo que ir al médico a las 10:00. Además, por la tarde bajaré a comprar comida."
doc = npl(nota)


for token in doc:
    if token.pos_ in ["VERB", "AUX"]:
        tarea_estructurada["acciones"].append(token.text)


resultados = matcher(doc)

for match_id, start, end in resultados:
    etiqueta = npl.vocab.strings[match_id]
    palabra = doc[start:end].text
    print(f"- {palabra} (Tipo: {etiqueta})")

    # clasificacion etiqueta
    if etiqueta == "DIA":
        tarea_estructurada["dias"].append(palabra)
    elif etiqueta == "HORA":
        tarea_estructurada["horas"].append(palabra)


# extraer archivo JSON
with open("tarea_estructurada.json", "w", encoding="utf-8") as archivo_json:
    json.dump(tarea_estructurada, archivo_json, ensure_ascii=False, indent=4)

print("Tarea estructurada guardada en 'tarea_estructurada.json'")

