import streamlit as st
import spacy
from spacy.matcher import Matcher
import datetime

st.set_page_config(page_title="Mi Organizador NLP", page_icon="🧠", layout="wide")

@st.cache_resource
def cargar_ia():
    nlp = spacy.load("es_core_news_sm")
    matcher = Matcher(nlp.vocab)
    
    matcher.add("DIA", [[{"LOWER": {"IN": ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]}}]])
    matcher.add("HORA", [[{"SHAPE": "dd:dd"}]])
    matcher.add("MOMENTO", [[{"LOWER": {"IN": ["mañana", "tarde", "noche", "madrugada", "mediodía"]}}]])
    return nlp, matcher

nlp, matcher = cargar_ia()

MAPEO_DIAS = {
    "lunes": 0, "martes": 1, "miércoles": 2, "jueves": 3, 
    "viernes": 4, "sábado": 5, "domingo": 6
}

def calcular_proximo_dia(nombre_dia):
    hoy = datetime.date.today()
    dia_objetivo = MAPEO_DIAS.get(nombre_dia.lower())
    if dia_objetivo is None: return None
    
    dias_faltantes = (dia_objetivo - hoy.weekday()) % 7
    return hoy + datetime.timedelta(days=dias_faltantes)


if "tareas_guardadas" not in st.session_state:
    st.session_state.tareas_guardadas = []


# calendario lateral
st.sidebar.title("Calendario y Agenda")
fecha_seleccionada = st.sidebar.date_input(
    "Selecciona un día para ver tus tareas", 
    datetime.date.today()
)

st.sidebar.divider()
st.sidebar.subheader(f"Agenda: {fecha_seleccionada.strftime('%d/%m/%Y')}")

tareas_del_dia = [t for t in st.session_state.tareas_guardadas if t["fecha"] == fecha_seleccionada]

if tareas_del_dia:
    for t in tareas_del_dia:
        # st.sidebar.success crea una cajita verde muy visual
        st.sidebar.success(f"**{t['texto']}**\n\n🕒 {t['tiempos_extra']}")
else:
    st.sidebar.info("Día libre. No hay tareas programadas para esta fecha.")


# panel principal
st.title("Mi Organizador Inteligente")
st.write("Escribe tus notas en crudo. La IA extraerá tu checklist.")

nota_usuario = st.text_area("¿Qué tienes en mente para esta semana?", height=150)

if st.button("Procesar Tareas"):
    if nota_usuario:

        st.session_state.tareas_guardadas = [] 
        
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
            fecha_real_tarea = None 
            
            resultados = matcher(doc)
            for match_id, start, end in resultados:
                etiqueta = nlp.vocab.strings[match_id]
                palabra = doc[start:end].text
                
                if etiqueta == "DIA":
                    fecha_real_tarea = calcular_proximo_dia(palabra)
                    palabra = f"{palabra} ({fecha_real_tarea.strftime('%d/%m/%Y')})"
                        
                tiempos_linea.append(palabra)
                
            if acciones_linea:
                token_accion = acciones_linea[0] 
                contexto_tarea = doc[token_accion.i : ].text.strip()
                

                st.session_state.tareas_guardadas.append({
                    "texto": contexto_tarea.capitalize(),
                    "fecha": fecha_real_tarea, # Fecha en formato máquina
                    "tiempos_extra": " • ".join(tiempos_linea) if tiempos_linea else ""
                })
    else:
        st.warning("¡Escribe algo en la caja de texto primero!")


# checklist global
if st.session_state.tareas_guardadas:
    st.divider() 
    st.subheader("Tu Checklist Completa")
    
    for i, tarea in enumerate(st.session_state.tareas_guardadas):
        with st.container(border=True):
            st.checkbox(f"**{tarea['texto']}**", key=f"chk_main_{i}")
            if tarea['tiempos_extra']:
                st.caption(f"*Cuándo:* {tarea['tiempos_extra']}")