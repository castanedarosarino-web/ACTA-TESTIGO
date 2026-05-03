import streamlit as st
import json
from datetime import datetime

# 1. CONFIGURACIÓN DE PÁGINA Y ESTÉTICA "DASHBOARD"
st.set_page_config(page_title="S.I.V. - Gestión de Testigos", layout="wide")

# CSS para imitar la estética de la foto (Escritorio Médico/Policial)
st.markdown("""
    <style>
    /* Fondo y contenedores */
    .stApp { background-color: #f0f2f6; }
    
    /* Estilo de Tarjetas de Módulo */
    .module-card {
        background-color: #0d47a1;
        color: white;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        margin-bottom: 10px;
    }
    
    /* Personalización de Inputs y Textareas */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        border-radius: 8px !important;
        border: 1px solid #0d47a1 !important;
    }
    
    /* Títulos con color corporativo */
    h1, h2, h3 { color: #0d47a1 !important; }
    
    /* Sidebar estilizada */
    [data-testid="stSidebar"] {
        background-color: #e3f2fd;
        border-right: 2px solid #0d47a1;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown('<div style="text-align:center"><h1>🚓 S.I.V.</h1><p>Control de Gestión</p></div>', unsafe_allow_html=True)
    st.header("Oficial Interviniente")
    interviniente = st.text_input("Rango y Nombre", value="SUB COMISARIO CASTAÑEDA JUAN", disabled=True)
    st.markdown("---")
    st.subheader("📍 Lugar del Hecho")
    lugar = st.text_input("Dirección", placeholder="SARMIENTO 3361, ZAVALLA")
    st.subheader("⏰ Hora")
    hora_hecho = st.text_input("HH:MM", placeholder="08:00")

def generar_texto_acta(t_num, datos, interviniente, lugar):
    fecha_actual = datetime.now().strftime("%d/%m/%Y")
    hora_actual = datetime.now().strftime("%H:%M")
    return f"""ACTA DE ENTREVISTA TÉCNICA
---------------------------------------
LUGAR: {lugar if lugar else 'S/D'}
FECHA: {fecha_actual} | HORA: {hora_actual}
INTERVINIENTE: {interviniente}

SE PROCEDE A ENTREVISTAR AL TESTIGO N° {t_num}:
NOMBRE: {datos['filiacion']['nombre']}
DNI: {datos['filiacion']['dni']}
DOMICILIO: {datos['filiacion']['domicilio']}

RELATO DE ENTREVISTA:
{datos['contenido']}
---------------------------------------
"""

def main():
    # Encabezado tipo Dashboard
    c_head1, c_head2 = st.columns([1, 4])
    with c_head1:
        st.markdown('<div class="module-card"><div style="font-size:50px">👤</div></div>', unsafe_allow_html=True)
    with c_head2:
        st.title("GESTIÓN DE TESTIGOS (Módulo Espejo)")
        st.caption("Autor: Sub Comisario CASTAÑEDA Juan | Versión Profesional 2026")

    st.markdown("---")

    if 'lista_testigos' not in st.session_state:
        st.session_state.lista_testigos = [1]

    datos_acumulados = {}

    for t_num in st.session_state.lista_testigos:
        # Usamos contenedores con bordes para organizar la información
        with st.container():
            st.subheader(f"🆔 Testigo N° {t_num}")
            
            c1, c2, c3 = st.columns([2, 1, 1])
            nombre = c1.text_input("Apellido y Nombres", key=f"n_{t_num}").upper()
            dni = c2.text_input("D.N.I.", key=f"d_{t_num}")
            sexo = c3.selectbox("Edad/Sexo", ["MASCULINO", "FEMENINO", "OTRO"], key=f"s_{t_num}")

            c4, c5, c6 = st.columns([2, 1, 1])
            dom = c4.text_input("Domicilio Real", key=f"do_{t_num}").upper()
            nac = c5.text_input("Nacionalidad", value="ARGENTINA", key=f"na_{t_num}").upper()
            ec = c6.selectbox("Estado Civil", ["SOLTERO/A", "CASADO/A", "DIVORCIADO/A"], key=f"ec_{t_num}")

            st.markdown("#### ✍️ Relato del Hecho")
            declara = st.radio(f"¿Presta declaración?", ["NO", "SI"], key=f"dec_{t_num}", horizontal=True)

            relato_final = ""
            if declara == "SI":
                relato_espontaneo = st.text_area("Ingrese el relato espontáneo:", key=f"re_{t_num}", height=100)
                
                if st.button(f"✨ Pulir Relato Técnico T{t_num}"):
                    # Aplicamos el criterio técnico de Tentativa de Robo (Bronce/Sagrario)
                    pulido = f"QUE EN LA FECHA, MANIFIESTA QUE: {relato_espontaneo.upper()}. TRAS INSPECCIÓN, SE CONSTATA EL DESMONTE DE PERNOS Y BISAGRAS MEDIANTE EL USO DE HERRAMIENTAS, ACCIÓN DIRIGIDA AL APODERAMIENTO DE PIEZA DE BRONCE, VENCIENDO LA SEGURIDAD MECÁNICA."
                    st.session_state[f"ia_out_{t_num}"] = pulido
                
                relato_final = st.text_area("Relato Procesado (Formato Judicial):", 
                                             value=st.session_state.get(f"ia_out_{t_num}", ""), 
                                             key=f"rip_{t_num}", height=120)

            datos_acumulados[f"testigo_{t_num}"] = {
                "filiacion": {"nombre": nombre, "dni": dni, "domicilio": dom, "es": sexo},
                "declara": declara, "contenido": relato_final
            }
            st.markdown("---")

    # CONTROLES DE INTERFAZ
    col_add, col_del = st.columns(2)
    if col_add.button("➕ AGREGAR OTRO TESTIGO"):
        st.session_state.lista_testigos.append(len(st.session_state.lista_testigos) + 1)
        st.rerun()
    
    if len(st.session_state.lista_testigos) > 1:
        if col_del.button("🗑️ QUITAR ÚLTIMO TESTIGO"):
            st.session_state.lista_testigos.pop()
            st.rerun()

    # --- PANEL DE EXPORTACIÓN (ESTILO DASHBOARD) ---
    st.markdown("### 📥 Panel de Descargas")
    
    # Preparación de datos (Pre-carga para evitar error en Render)
    json_final = json.dumps(datos_acumulados, indent=4)
    actas_txt = ""
    for t_id, t_info in datos_acumulados.items():
        if t_info['declara'] == "SI":
            actas_txt += generar_texto_acta(t_id, t_info, interviniente, lugar) + "\n\n"

    cj1, cj2 = st.columns(2)
    with cj1:
        st.download_button("📂 EXPORTAR PAQUETE JSON PARA WHATSAPP", data=json_final, 
                           file_name=f"testigos_{datetime.now().strftime('%d%m%Y')}.json", mime="application/json")
    
    with cj2:
        if actas_txt:
            st.download_button("🖨️ GENERAR ACTAS TÉCNICAS (TXT)", data=actas_txt, 
                               file_name=f"actas_{datetime.now().strftime('%H%M')}.txt", mime="text/plain")
        else:
            st.button("🖨️ GENERAR PDF (Sin datos)", disabled=True)

if __name__ == "__main__":
    main()
