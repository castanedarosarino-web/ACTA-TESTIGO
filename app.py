import streamlit as st
import json
from datetime import datetime

# CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="S.I.V. - Bloque 4: TESTIGOS", layout="wide")

# --- SIDEBAR (COHERENCIA CON BLOQUE 3) ---
with st.sidebar:
    st.header("Oficial Interviniente")
    st.text_input("Rango y Nombre", value="SUB COMISARIO CASTAÑEDA JUAN", disabled=True)
    st.markdown("---")
    st.subheader("Lugar del Hecho")
    lugar = st.text_input("Dirección", placeholder="EJ: CALLE SALTA 1200, ROSARIO")
    st.subheader("Hora del Hecho")
    hora = st.text_input("HH:MM", placeholder="10:30")

def main():
    # ENCABEZADO IDÉNTICO AL BLOQUE 3
    st.title("🚓 S.I.V. - Bloque 4: GESTIÓN DE TESTIGOS")
    st.caption("Autor: Sub Comisario CASTAÑEDA Juan")
    st.markdown("---")

    # Inicialización dinámica de testigos
    if 'lista_testigos' not in st.session_state:
        st.session_state.lista_testigos = [1]

    datos_acumulados = {}

    # RENDERIZADO DE TESTIGOS
    for t_num in st.session_state.lista_testigos:
        with st.expander(f"🆔 {t_num}. DATOS FILIATORIOS DEL TESTIGO", expanded=True):
            # Fila 1: Nombres, DNI, Sexo
            c1, c2, c3 = st.columns([2, 1, 1])
            nombre = c1.text_input("Apellido y Nombres", key=f"n_{t_num}").upper()
            dni = c2.text_input("DNI", key=f"d_{t_num}")
            sexo = c3.selectbox("Sexo", ["MASCULINO", "FEMENINO", "OTRO"], key=f"s_{t_num}")

            # Fila 2: Nacionalidad, Estado Civil, Fecha Nacimiento
            c4, c5, c6 = st.columns([1, 1, 1])
            nac = c4.text_input("Nacionalidad", value="ARGENTINA", key=f"na_{t_num}").upper()
            ec = c5.selectbox("Estado Civil", ["SOLTERO/A", "CASADO/A", "DIVORCIADO/A", "VIUDO/A"], key=f"ec_{t_num}")
            fnac = c6.date_input("Fecha de Nacimiento", key=f"fn_{t_num}")

            # Fila 3: Ocupación, Teléfono, Correo
            c7, c8, c9 = st.columns([1, 1, 1])
            ocu = c7.text_input("Ocupación", key=f"oc_{t_num}").upper()
            tel = c8.text_input("Teléfono Celular", key=f"te_{t_num}")
            mail = c9.text_input("Correo Electrónico", key=f"ma_{t_num}")

            # Fila 4: Domicilio (Ancho completo)
            dom = st.text_input("Domicilio Real", key=f"do_{t_num}").upper()

        # SECCIÓN DE RELATO (ESPEJO BLOQUE 3)
        st.subheader(f"✍️ {t_num}. Relato del Testigo")
        declara = st.radio(f"¿El testigo {t_num} presta declaración?", ["NO", "SI"], key=f"dec_{t_num}", horizontal=True)

        if declara == "SI":
            relato_espontaneo = st.text_area("Ingrese el relato espontáneo:", key=f"re_{t_num}", height=150)
            
            col_ia1, col_ia2 = st.columns(2)
            if col_ia1.button(f"✨ Pulir Relato T{t_num}"):
                # Aquí se conecta la IA. Simulamos el regreso.
                st.session_state[f"ia_out_{t_num}"] = f"EN LA FECHA, MANIFIESTA QUE: {relato_espontaneo.upper()}"
            
            relato_pulido = st.text_area("Relato Procesado (Formato Judicial):", 
                                         value=st.session_state.get(f"ia_out_{t_num}", ""), 
                                         key=f"rip_{t_num}", height=150)

        # Botón para la referencia en el Acta Principal (Opción B)
        if st.button(f"📌 Generar Referencia para Acta de Procedimiento (T{t_num})"):
            ref = f"{nombre}, DNI {dni}, testigo a quien se le recepciona entrevista técnica a los fines de precisar su testimonio sobre lo acontecido."
            st.success("Copia la siguiente referencia:")
            st.code(ref)

        # Guardamos en diccionario para el JSON final
        datos_acumulados[f"testigo_{t_num}"] = {
            "filiacion": {"nombre": nombre, "dni": dni, "domicilio": dom, "tel": tel},
            "declara": declara,
            "contenido": st.session_state.get(f"ia_out_{t_num}", "") if declara == "SI" else "NO DECLARA"
        }
        st.markdown("---")

    # CONTROLES DINÁMICOS
    col_add, col_del = st.columns(2)
    if col_add.button("➕ AGREGAR OTRO TESTIGO"):
        proximo = len(st.session_state.lista_testigos) + 1
        st.session_state.lista_testigos.append(proximo)
        st.rerun()
    
    if len(st.session_state.lista_testigos) > 1:
        if col_del.button("🗑️ QUITAR ÚLTIMO TESTIGO"):
            st.session_state.lista_testigos.pop()
            st.rerun()

    # CIERRE DE BLOQUE Y EXPORTACIÓN
    st.subheader("💾 Cierre de Módulo")
    cj1, cj2 = st.columns(2)
    
    with cj1:
        # Generar JSON para el Actante
        json_final = json.dumps(datos_acumulados, indent=4)
        st.download_button("📥 GENERAR JSON PARA ACTANTE", data=json_final, file_name=f"testigos_{datetime.now().strftime('%d%m%Y')}.json")
    
    with cj2:
        if st.button("📄 GENERAR PDFs DE ENTREVISTA"):
            st.warning("Función de exportación masiva a PDF en proceso de enlace.")

if __name__ == "__main__":
    main()
