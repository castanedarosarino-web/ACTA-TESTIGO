import streamlit as st
import json
from datetime import datetime
from fpdf import FPDF
import io

# CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="S.I.V. - Bloque 4: GESTIÓN DE TESTIGOS", layout="wide")

# --- SIDEBAR ---
with st.sidebar:
    st.header("Oficial Interviniente")
    interviniente = st.text_input("Rango y Nombre", value="SUB COMISARIO CASTAÑEDA JUAN", disabled=True)
    st.markdown("---")
    st.subheader("Lugar del Hecho")
    lugar = st.text_input("Dirección", placeholder="EJ: CALLE SARMIENTO 3361, ZAVALLA")
    st.subheader("Hora del Hecho")
    hora_hecho = st.text_input("HH:MM", placeholder="08:00")

def generar_pdf_bytes(datos_acumulados, interviniente, lugar):
    """Genera un archivo PDF real en memoria para descargar"""
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    fecha_actual = datetime.now().strftime("%d/%m/%Y")
    hora_actual = datetime.now().strftime("%H:%M")

    for t_id, t_info in datos_acumulados.items():
        if t_info['declara'] == "SI":
            pdf.add_page()
            # Encabezado
            pdf.set_font("Arial", 'B', 14)
            pdf.cell(0, 10, "ACTA DE ENTREVISTA TÉCNICA", ln=True, align='C')
            pdf.set_font("Arial", '', 10)
            pdf.cell(0, 10, f"LUGAR: {lugar if lugar else 'S/D'} | FECHA: {fecha_actual} | HORA: {hora_actual}", ln=True)
            pdf.cell(0, 10, f"INTERVINIENTE: {interviniente}", ln=True)
            pdf.line(10, 40, 200, 40)
            pdf.ln(5)

            # Datos del Testigo
            pdf.set_font("Arial", 'B', 11)
            pdf.cell(0, 10, f"DATOS DEL TESTIGO ({t_id.replace('_', ' ').upper()}):", ln=True)
            pdf.set_font("Arial", '', 11)
            pdf.cell(0, 8, f"NOMBRE: {t_info['filiacion']['nombre']}", ln=True)
            pdf.cell(0, 8, f"DNI: {t_info['filiacion']['dni']} | SEXO: {t_info['filiacion']['es']}", ln=True)
            pdf.cell(0, 8, f"DOMICILIO: {t_info['filiacion']['domicilio']}", ln=True)
            pdf.cell(0, 8, f"OCUPACIÓN: {t_info['filiacion']['ocupacion']}", ln=True)
            pdf.ln(5)

            # Relato
            pdf.set_font("Arial", 'B', 11)
            pdf.cell(0, 10, "RELATO DE LA ENTREVISTA:", ln=True)
            pdf.set_font("Arial", '', 11)
            pdf.multi_cell(0, 7, t_info['contenido'])
            
            # Firmas
            pdf.ln(20)
            pdf.cell(90, 10, "------------------------------------", 0, 0, 'C')
            pdf.cell(90, 10, "------------------------------------", 0, 1, 'C')
            pdf.cell(90, 5, "FIRMA ENTREVISTADO", 0, 0, 'C')
            pdf.cell(90, 5, "FIRMA INTERVINIENTE", 0, 1, 'C')

    return pdf.output(dest='S').encode('latin-1', errors='replace')

def main():
    st.title("🚓 S.I.V. - Bloque 4: GESTIÓN DE TESTIGOS")
    st.caption("Autor: Sub Comisario CASTAÑEDA Juan")
    st.markdown("---")

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
            
            if st.button(f"✨ Pulir Relato T{t_num}"):
                # Criterio técnico tentativa de robo según fotos enviadas
                texto_pulido = f"QUE EN LA FECHA, MANIFIESTA QUE: {relato_espontaneo.upper()}. SE OBSERVA EL DESMONTE DE PERNOS Y BISAGRAS MEDIANTE EL USO DE HERRAMIENTAS, ACCIÓN DIRIGIDA AL DESPRENDIMIENTO Y APODERAMIENTO DE LA PIEZA DE BRONCE, VENCIENDO LA SEGURIDAD MECÁNICA DEL ELEMENTO."
                st.session_state[f"ia_out_{t_num}"] = texto_pulido
            
            relato_final = st.text_area("Relato Procesado (Formato Judicial):", 
                                         value=st.session_state.get(f"ia_out_{t_num}", ""), 
                                         key=f"rip_{t_num}", height=150)

        datos_acumulados[f"testigo_{t_num}"] = {
            "filiacion": {"nombre": nombre, "dni": dni, "domicilio": dom, "tel": tel, "es": sexo, "ocupacion": ocu},
            "declara": declara,
            "contenido": relato_final
        }
        st.markdown("---")

    col_add, col_del = st.columns(2)
    if col_add.button("➕ AGREGAR OTRO TESTIGO"):
        st.session_state.lista_testigos.append(len(st.session_state.lista_testigos) + 1)
        st.rerun()
    
    if len(st.session_state.lista_testigos) > 1:
        if col_del.button("🗑️ QUITAR ÚLTIMO TESTIGO"):
            st.session_state.lista_testigos.pop()
            st.rerun()

    st.subheader("💾 Cierre de Módulo y Descargas")
    cj1, cj2 = st.columns(2)
    
    with cj1:
        json_final = json.dumps(datos_acumulados, indent=4)
        st.download_button("📥 GENERAR JSON PARA ACTANTE", data=json_final, 
                           file_name=f"testigos_{datetime.now().strftime('%d%m%Y')}.json", mime="application/json")
    
    with cj2:
        # Generación de PDF Real
        if any(t['declara'] == "SI" for t in datos_acumulados.values()):
            pdf_data = generar_pdf_bytes(datos_acumulados, interviniente, lugar)
            st.download_button(
                label="📄 DESCARGAR ACTAS EN PDF",
                data=pdf_data,
                file_name=f"actas_SIV_{datetime.now().strftime('%H%M')}.pdf",
                mime="application/pdf"
            )
        else:
            st.button("📄 DESCARGAR ACTAS (Sin declaraciones)", disabled=True)

if __name__ == "__main__":
    main()
