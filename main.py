import spacy

print("Cargando modelo de IA...")
npl = spacy.load("es_core_news_sm")

nota = "El miércoles tengo turno a las 20:30 y el viernes tengo que ir al médico a las 10:00. Además, por la tarde bajaré a comprar comida."

doc = npl(nota)

print("Palabras detectadas: ")
for token in doc:
    print(f"- {token.text}")