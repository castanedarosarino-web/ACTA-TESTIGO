
import streamlit as st
from datetime import datetime
import json

# --- CONFIGURACIÓN DE PÁGINA PARA RENDER ---
st.set_page_config(
    page_title="SVI - Bloque 4: Testigos",
    page_icon="👥",
    layout="wide"
)

# --- ESTILOS PERSONALIZADOS ---
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; }
    .stTextArea>div>div>textarea { background-color: #ffffff; }
    </style>
    """, unsafe_allow_html=True)

def main():
    st.title("👥 Sistema de Validación de Identidad - Bloque 4")
    st.subheader("Módulo de Testigos de Actuación y Entrevistas Técnicas")
    st.info("SubComisario Castañeda Juan - Protocolo URII Santa Fe")

    # --- INICIALIZACIÓN DE SESSION STATE ---
    if 'testigo_activo' not in st.session_state:
        st.session_state.testigo_activo = 1
    if 'testigos_data' not in st.session_state:
        st.session_state.testigos_data = {i: {} for i in range(1, 5)}

    # --- BOTONERA DE SELECCIÓN DE TESTIGO ---
    cols = st.columns(4)
    for i in range(1, 5):
        if cols[i-1].button(f"👤 Testigo {i}", type="primary" if st.session_state.testigo_activo == i else "secondary"):
            st.session_state.testigo_activo = i

    t_idx = st.session_state.testigo_activo
    
    st.markdown(f"### Editando: **TESTIGO N° {t_idx}**")

    # --- FORMULARIO DE FILIACIÓN (ESPEJO ACTA DE ENTREVISTA) ---
    with st.expander("🆔 Datos Filiatorios", expanded=True):
        c1, c2, c3 = st.columns([2, 1, 1])
        nombre = c1.text_input("Apellido y Nombres", key=f"n_{t_idx}").upper()
        dni = c2.text_input("D.N.I.", key=f"d_{t_idx}")
        edad_sexo = c3.text_input("Edad / Sexo", key=f"es_{t_idx}").upper()

        c4, c5, c6 = st.columns([2, 1, 1])
        domicilio = c4.text_input("Domicilio Real", key=f"dom_{t_idx}").upper()
        nacionalidad = c5.text_input("Nacionalidad", value="ARGENTINA", key=f"nac_{t_idx}").upper()
        est_civil = st.selectbox("Estado Civil", ["SOLTERO/A", "CASADO/A", "DIVORCIADO/A", "VIUDO/A", "CONVIVIENTE"], key=f"ec_{t_idx}")

        c7, c8 = st.columns(2)
        ocupacion = c7.text_input("Ocupación / Oficio", key=f"ocu_{t_idx}").upper()
        contacto = c8.text_input("Contacto (Celular/Email)", key=f"con_{t_idx}")

    # --- MÓDULO DE DECLARACIÓN Y SALTO DE CALIDAD ---
    st.markdown("---")
    declara = st.checkbox("¿El testigo presta declaración técnica?", key=f"dec_check_{t_idx}")

    if declara:
        st.subheader("🎤 Relato y Entrevista")
        relato_crudo = st.text_area(
            "Describa lo que el testigo observó (Conflictos, mecánica, detalles):",
            placeholder="Sin inducir el relato. Describa el hecho tal cual lo expresa el testigo...",
            height=200,
            key=f"rel_{t_idx}"
        )
        
        if st.button(f"✨ Pulir Contenido con IA (T{t_idx})"):
            # Lógica de pulido simulada para el bloque independiente
            if relato_crudo:
                st.subheader("📄 Texto Pulido para el Acta de Entrevista:")
                texto_ia = f"Que en la fecha y hora de mención, en circunstancias que se encontraba en {domicilio}, manifiesta que: {relato_crudo}. Es todo cuanto tiene que declarar."
                st.text_area("Resultado IA (Copiar si es necesario):", value=texto_ia.upper(), height=150)
            else:
                st.error("Debe ingresar un relato para procesar.")

    # --- ACCIONES FINALES ---
    st.markdown("---")
    acc1, acc2, acc3 = st.columns(3)

    # 1. Inyección de Frase Opción B
    if acc1.button("📝 Generar Referencia para Bloque 1"):
        if nombre and dni:
            frase_b = f"{nombre}, DNI {dni}, testigo a quien se le recepciona entrevista técnica a los fines de precisar su testimonio sobre lo acontecido."
            st.code(frase_b, language="text")
            st.success("Copia esta frase en el acta de procedimiento.")
        else:
            st.warning("Faltan datos básicos del testigo.")

    # 2. Descarga de Datos JSON (Para el Actante)
    data_testigo = {
        "id": t_idx,
        "nombre": nombre,
        "dni": dni,
        "declara": declara,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    json_str = json.dumps(data_testigo, indent=4)
    acc2.download_button(
        label=f"📥 Guardar JSON Testigo {t_idx}",
        data=json_str,
        file_name=f"testigo_{t_idx}_{dni}.json",
        mime="application/json"
    )

    # 3. Generación de PDF (Espacio reservado)
    if acc3.button("📄 Previsualizar Acta de Entrevista"):
        st.info("Generando vista previa del acta según modelo ACTA_29487394.pdf...")

    # --- FIRMA DIGITAL (PUERTA ABIERTA) ---
    st.markdown("---")
    with st.expander("✍️ Módulo de Firma Digital"):
        st.write("Para uso en tablet o celular directamente en el lugar del hecho.")
        st.info("Lienzo de dibujo (Canvas) preparado para implementación tras validar estabilidad en Render.")
        if st.button("Simular Captura de Firma"):
            st.success(f"Firma del Testigo {t_idx} vinculada correctamente.")

if __name__ == "__main__":
    main()
