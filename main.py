import spacy
from spacy.matcher import Matcher

print("Cargando modelo de IA...")
npl = spacy.load("es_core_news_sm")

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

print("\n ACCIONES detectadas: ")
for token in doc:
    if token.pos_ in ["VERB", "AUX"]:
        print(f"- {token.text} (Raíz: {token.lemma_})")

print("\n Datos extraidos con Matcher: ")
resultados = matcher(doc)

for match_id, start, end in resultados:
    etiqueta = npl.vocab.strings[match_id]
    palabra = doc[start:end].text
    print(f"- {palabra} (Tipo: {etiqueta})")

