import streamlit as st
import json
from datetime import datetime

# Configuración idéntica a Bloques anteriores
st.set_page_config(page_title="SVI - Bloque 4: Testigos", layout="wide")

def main():
    st.title("👥 Gestión de Testigos (Módulo Espejo)")
    
    # Inicialización de la lista de testigos si no existe
    if 'lista_testigos' not in st.session_state:
        st.session_state.lista_testigos = [1] # Empieza con 1 por defecto

    # Contenedor para el JSON final
    datos_para_actante = {}

    for i, t_num in enumerate(st.session_state.lista_testigos):
        with st.container():
            st.subheader(f"📍 Testigo N° {t_num}")
            
            # --- ESTRUCTURA ESPEJO FILIACIÓN ---
            col1, col2, col3 = st.columns([2, 1, 1])
            nombre = col1.text_input("Apellido y Nombres", key=f"nom_{t_num}").upper()
            dni = col2.text_input("D.N.I.", key=f"dni_{t_num}")
            es = col3.text_input("Edad/Sexo", key=f"es_{t_num}").upper()

            col4, col5, col6 = st.columns([2, 1, 1])
            dom = col4.text_input("Domicilio Real", key=f"dom_{t_num}").upper()
            nac = col5.text_input("Nacionalidad", value="ARGENTINA", key=f"nac_{t_num}").upper()
            ec = col6.selectbox("Estado Civil", ["SOLTERO/A", "CASADO/A", "DIVORCIADO/A", "VIUDO/A"], key=f"ec_{t_num}")

            col7, col8 = st.columns(2)
            ocu = col7.text_input("Ocupación", key=f"ocu_{t_num}").upper()
            con = col8.text_input("Contacto (Cel/Email)", key=f"con_{t_num}")

            # --- LÓGICA DECLARA (IGUAL A VÍCTIMA) ---
            declara = st.radio("¿Presta declaración de entrevista?", ["NO", "SI"], key=f"dec_{t_num}", horizontal=True)

            if declara == "SI":
                st.markdown("#### 🎤 Relato de Entrevista")
                relato_crudo = st.text_area("Relato Crudo (Dichos del testigo):", key=f"raw_{t_num}", height=150)
                
                c_ia, c_res = st.columns([1, 1])
                if c_ia.button(f"✨ Pulir Relato Testigo {t_num}"):
                    # Simulación de retorno de IA (En fusión irá el prompt real)
                    st.session_state[f"ia_res_{t_num}"] = f"QUE EN LA FECHA, MANIFIESTA QUE: {relato_crudo.upper()}"
                
                resultado_ia = st.text_area("Relato Pulido por IA (Listo para PDF):", 
                                            value=st.session_state.get(f"ia_res_{t_num}", ""), 
                                            key=f"final_{t_num}", height=150)

            # Botón para inyectar la Opción B al Bloque 1
            if st.button(f"📝 Generar Referencia Acta (T{t_num})"):
                ref = f"{nombre}, DNI {dni}, testigo a quien se le recepciona entrevista técnica a los fines de precisar su testimonio sobre lo acontecido."
                st.code(ref)

            # Guardar en diccionario para JSON
            datos_para_actante[f"testigo_{t_num}"] = {
                "filiacion": {"nombre": nombre, "dni": dni, "domicilio": dom},
                "declara": declara,
                "entrevista": st.session_state.get(f"ia_res_{t_num}", "") if declara == "SI" else ""
            }
            st.markdown("---")

    # --- BOTONES DE CONTROL DE TESTIGOS ---
    c_add, c_del = st.columns(2)
    if c_add.button("➕ AGREGAR OTRO TESTIGO"):
        st.session_state.lista_testigos.append(len(st.session_state.lista_testigos) + 1)
        st.rerun()
    
    if len(st.session_state.lista_testigos) > 1:
        if c_del.button("🗑️ ELIMINAR ÚLTIMO TESTIGO"):
            st.session_state.lista_testigos.pop()
            st.rerun()

    # --- ACCIONES FINALES (IGUAL A BLOQUE 1, 2 Y 3) ---
    st.subheader("💾 Finalizar Bloque 4")
    col_json, col_pdf = st.columns(2)
    
    with col_json:
        json_str = json.dumps(datos_para_actante, indent=4)
        st.download_button("📥 GENERAR JSON PARA ACTANTE", data=json_str, file_name="bloque4_testigos.json", mime="application/json")
    
    with col_pdf:
        if st.button("📄 GENERAR PDF DE ENTREVISTAS"):
            st.info("Generando PDFs independientes para testigos que declararon...")

if __name__ == "__main__":
    main()
