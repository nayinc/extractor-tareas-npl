import streamlit as st
import spacy
from spacy.matcher import Matcher

# conf visual 
st.set_page_config(page_title="Mi Organizador NLP", page_icon="🧠")


@st.cache_resource
def cargar_ia():
    nlp = spacy.load("es_core_news_sm")
    matcher = Matcher(nlp.vocab)
    
    # Nuestras reglas del Matcher
    matcher.add("DIA", [[{"LOWER": {"IN": ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]}}]])
    matcher.add("HORA", [[{"SHAPE": "dd:dd"}]])
    matcher.add("MOMENTO", [[{"LOWER": {"IN": ["mañana", "tarde", "noche", "madrugada", "mediodía"]}}]])
    
    return nlp, matcher


nlp, matcher = cargar_ia()

# diseño web
st.title("📝 Mi Organizador Inteligente")
st.write("Escribe tus notas en crudo. La IA extraerá tu checklist.")


nota_usuario = st.text_area("¿Qué tienes en mente para esta semana?", height=150)

if st.button("Procesar Tareas"):
    if nota_usuario:
        st.divider() 
        st.subheader("Tu Checklist Inteligente")
        
        hay_alguna_tarea = False
        
        lineas = [linea for linea in nota_usuario.split('\n') if linea.strip() != ""]
        
        for num_linea, linea in enumerate(lineas):
            doc = nlp(linea)
            
            acciones_linea = []
            
            verbos_debil = ["haber", "ser", "estar", "ir", "tener"]
            
            todos_los_verbos = [token for token in doc if token.pos_ in ["VERB", "AUX"]]
            
            if todos_los_verbos:
                for token in todos_los_verbos:
                    if len(todos_los_verbos) > 1 and token.lemma_.lower() in verbos_debil:
                        continue 
                    acciones_linea.append(token)
            
            tiempos_linea = []
            resultados = matcher(doc)
            for match_id, start, end in resultados:
                tiempos_linea.append(doc[start:end].text)
                
            if acciones_linea:
                hay_alguna_tarea = True
                
                with st.container(border=True):
                    token_accion = acciones_linea[0] 
                    
                    fin_contexto = min(token_accion.i + 7, len(doc))
                    contexto_tarea = doc[token_accion.i : fin_contexto].text
                    
                    st.checkbox(f"**{contexto_tarea.capitalize()}...**", key=f"chk_{num_linea}")
                    
                    if tiempos_linea:
                        contexto_tiempo = " • ".join(tiempos_linea)
                        st.caption(f"🕒 *Cuándo:* {contexto_tiempo}")
                        
        if not hay_alguna_tarea:
            st.info("No he detectado acciones concretas en tu texto.")
            
    else:
        st.warning("¡Escribe algo en la caja de texto primero!")