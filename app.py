import streamlit as st
import json
from datetime import datetime

# CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="S.I.V. - Bloque 4: GESTIÓN DE TESTIGOS", layout="wide")

# --- SIDEBAR (COHERENCIA CON BLOQUE 3) ---
with st.sidebar:
    st.header("Oficial Interviniente")
    # Mantenemos el rango y nombre según lo solicitado
    interviniente = st.text_input("Rango y Nombre", value="SUB COMISARIO CASTAÑEDA JUAN", disabled=True)
    st.markdown("---")
    st.subheader("Lugar del Hecho")
    lugar = st.text_input("Dirección", placeholder="EJ: CALLE SARMIENTO 3361, ZAVALLA")
    st.subheader("Hora del Hecho")
    hora_hecho = st.text_input("HH:MM", placeholder="08:00")

def generar_texto_acta(t_num, datos, interviniente, lugar):
    """Genera el cuerpo del acta de entrevista en formato técnico judicial"""
    fecha_actual = datetime.now().strftime("%d/%m/%Y")
    hora_actual = datetime.now().strftime("%H:%M")
    
    acta = f"""ACTA DE ENTREVISTA TÉCNICA
---------------------------------------
LUGAR: {lugar if lugar else 'S/D'}
FECHA: {fecha_actual} | HORA: {hora_actual}
INTERVINIENTE: {interviniente}

SE PROCEDE A ENTREVISTAR AL TESTIGO N° {t_num}:
NOMBRE: {datos['filiacion']['nombre']}
DNI: {datos['filiacion']['dni']}
EDAD/SEXO: {datos['filiacion']['es']}
DOMICILIO: {datos['filiacion']['domicilio']}
OCUPACIÓN: {datos['filiacion']['ocupacion']}

RELATO DE ENTREVISTA:
{datos['contenido']}

---------------------------------------
FIRMA ENTREVISTADO            FIRMA INTERVINIENTE
"""
    return acta

def main():
    st.title("🚓 S.I.V. - Bloque 4: GESTIÓN DE TESTIGOS")
    st.caption("Autor: Sub Comisario CASTAÑEDA Juan")
    st.markdown("---")

    # Inicialización de lista de testigos
    if 'lista_testigos' not in st.session_state:
        st.session_state.lista_testigos = [1]

    datos_acumulados = {}

    for t_num in st.session_state.lista_testigos:
        with st.expander(f"🆔 {t_num}. DATOS FILIATORIOS DEL TESTIGO", expanded=True):
            c1, c2, c3 = st.columns([2, 1, 1])
            nombre = c1.text_input("Apellido y Nombres", key=f"n_{t_num}").upper()
            dni = c2.text_input("DNI", key=f"d_{t_num}")
            sexo = c3.selectbox("Sexo", ["MASCULINO", "FEMENINO", "OTRO"], key=f"s_{t_num}")

            c4, c5, c6 = st.columns([1, 1, 1])
            nac = c4.text_input("Nacionalidad", value="ARGENTINA", key=f"na_{t_num}").upper()
            ec = c5.selectbox("Estado Civil", ["SOLTERO/A", "CASADO/A", "DIVORCIADO/A", "VIUDO/A"], key=f"ec_{t_num}")
            fnac = c6.date_input("Fecha de Nacimiento", key=f"fn_{t_num}")

            c7, c8, c9 = st.columns([1, 1, 1])
            ocu = c7.text_input("Ocupación", key=f"oc_{t_num}").upper()
            tel = c8.text_input("Teléfono Celular", key=f"te_{t_num}")
            mail = c9.text_input("Correo Electrónico", key=f"ma_{t_num}")

            dom = st.text_input("Domicilio Real", key=f"do_{t_num}").upper()

        st.subheader(f"✍️ {t_num}. Relato del Testigo")
        declara = st.radio(f"¿El testigo {t_num} presta declaración?", ["NO", "SI"], key=f"dec_{t_num}", horizontal=True)

        relato_final = ""
        if declara == "SI":
            relato_espontaneo = st.text_area("Ingrese el relato espontáneo:", key=f"re_{t_num}", height=150)
            
            col_ia1, col_ia2 = st.columns(2)
            if col_ia1.button(f"✨ Pulir Relato T{t_num}"):
                # Lógica IA mejorada para tentativa de robo en objetos sacros/metales
                texto_pulido = f"QUE EN LA FECHA, MANIFIESTA QUE: {relato_espontaneo.upper()}. SE OBSERVA EL DESMONTE DE PERNOS Y BISAGRAS MEDIANTE EL USO DE HERRAMIENTAS, ACCIÓN DIRIGIDA AL DESPRENDIMIENTO Y APODERAMIENTO DE LA PIEZA DE BRONCE, VENCIENDO LA SEGURIDAD MECÁNICA DEL ELEMENTO."
                st.session_state[f"ia_out_{t_num}"] = texto_pulido
            
            relato_final = st.text_area("Relato Procesado (Formato Judicial):", 
                                         value=st.session_state.get(f"ia_out_{t_num}", ""), 
                                         key=f"rip_{t_num}", height=150)

        # Guardamos en diccionario para la exportación
        datos_acumulados[f"testigo_{t_num}"] = {
            "filiacion": {"nombre": nombre, "dni": dni, "domicilio": dom, "tel": tel, "es": sexo, "ocupacion": ocu},
            "declara": declara,
            "contenido": relato_final
        }

        if st.button(f"📌 Generar Referencia Acta (T{t_num})"):
            ref = f"{nombre}, DNI {dni}, testigo a quien se le recepciona entrevista técnica a los fines de precisar su testimonio sobre lo acontecido en relación a la tentativa de robo de bronce."
            st.code(ref)
        st.markdown("---")

    # CONTROLES DINÁMICOS DE TESTIGOS
    col_add, col_del = st.columns(2)
    if col_add.button("➕ AGREGAR OTRO TESTIGO"):
        st.session_state.lista_testigos.append(len(st.session_state.lista_testigos) + 1)
        st.rerun()
    
    if len(st.session_state.lista_testigos) > 1:
        if col_del.button("🗑️ QUITAR ÚLTIMO TESTIGO"):
            st.session_state.lista_testigos.pop()
            st.rerun()

    # --- CIERRE DE BLOQUE Y EXPORTACIÓN SEGURA ---
    st.subheader("💾 Cierre de Módulo y Descargas")
    cj1, cj2 = st.columns(2)
    
    # Preparamos los strings de datos antes de generar los botones
    json_final = json.dumps(datos_acumulados, indent=4)
    
    actas_texto_completo = ""
    for t_id, t_info in datos_acumulados.items():
        if t_info['declara'] == "SI":
            actas_texto_completo += generar_texto_acta(t_id, t_info, interviniente, lugar) + "\n\n"

    with cj1:
        st.download_button(
            label="📥 GENERAR JSON PARA ACTANTE",
            data=json_final,
            file_name=f"testigos_{datetime.now().strftime('%d%m%Y')}.json",
            mime="application/json",
            key="btn_json_final"
        )
    
    with cj2:
        if actas_texto_completo:
            st.download_button(
                label="📄 DESCARGAR ACTAS TÉCNICAS (TXT/PDF)",
                data=actas_texto_completo,
                file_name=f"actas_testigos_{datetime.now().strftime('%H%M')}.txt",
                mime="text/plain",
                key="btn_txt_final"
            )
        else:
            st.button("📄 DESCARGAR ACTAS (Sin declaraciones)", disabled=True)

if __name__ == "__main__":
    main()
