import streamlit as st
import json
from datetime import datetime
from fpdf import FPDF
import io
import streamlit as st
import json
from datetime import datetime
from fpdf import FPDF
import io

# CONFIGURACIÓN DE PÁGINA
st.set_page_config(
    page_title="S.I.V. - Bloque 4: Gestión de Testigos",
    layout="wide"
)

# --- SIDEBAR ---
with st.sidebar:
    st.header("Oficial Interviniente")
    # CORRECCIÓN: Ahora es editable (disabled=False)
    interviniente = st.text_input(
        "Rango y Nombre",
        value="SUB COMISARIO CASTAÑEDA JUAN",
        disabled=False
    )

    st.markdown("---")
    st.subheader("Lugar del Hecho")
    lugar = st.text_input(
        "Dirección",
        placeholder="EJ: SARMIENTO 3361, ZAVALLA"
    )

    st.subheader("Hora del Hecho")
    hora_hecho = st.text_input("HH:MM", placeholder="08:00")

def limpiar_texto_pdf(texto):
    """Limpia caracteres especiales para evitar errores en FPDF"""
    if texto is None: return ""
    reemplazos = {
        "“": '"', "”": '"', "‘": "'", "’": "'",
        "–": "-", "—": "-", "…": "...", "°": "Nro.",
        "ñ": "n", "Ñ": "N", "á": "a", "é": "e", "í": "i", "ó": "o", "ú": "u",
        "Á": "A", "É": "E", "Í": "I", "Ó": "O", "Ú": "U"
    }
    texto = str(texto)
    for original, reemplazo in reemplazos.items():
        texto = texto.replace(original, reemplazo)
    return texto

def generar_pdf_bytes(datos_acumulados, interviniente, lugar, hora_hecho):
    """Genera PDF con formato legal judicial real"""
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.set_margins(left=25, top=20, right=15)
    pdf.set_auto_page_break(auto=True, margin=20)
    
    fecha_actual = datetime.now().strftime("%d/%m/%Y")
    hora_documento = hora_hecho if hora_hecho else datetime.now().strftime("%H:%M")
    
    hay_actas = False

    for t_id, t_info in datos_acumulados.items():
        if t_info["declara"] == "SI":
            hay_actas = True
            pdf.add_page()

            # ENCABEZADO FORMAL POLICIAL
            pdf.set_font("Arial", "B", 8)
            pdf.cell(0, 4, "POLICIA DE LA PROVINCIA", ln=True, align="L")
            pdf.cell(0, 4, "UNIDAD REGIONAL II - ROSARIO", ln=True, align="L")
            pdf.cell(0, 4, "SUBCOMISARIA ZAVALLA", ln=True, align="L")
            pdf.ln(8)

            pdf.set_font("Arial", "B", 14)
            pdf.cell(0, 10, "ACTA DE ENTREVISTA TECNICA", ln=True, align="C")
            pdf.ln(5)

            pdf.set_font("Arial", "", 11)
            pdf.multi_cell(0, 7, limpiar_texto_pdf(
                f"En Zavalla, Provincia de Santa Fe, a los {datetime.now().strftime('%d')} dias del mes de "
                f"{datetime.now().strftime('%B')} del año {datetime.now().strftime('%Y')}, siendo las "
                f"{hora_documento} horas, ante el interviniente {interviniente}, comparece la persona de:"
            ))
            pdf.ln(5)

            # FILIACIÓN (TABLA)
            pdf.set_font("Arial", "B", 11)
            pdf.cell(0, 8, "I. DATOS FILIATORIOS DEL INTERESADO:", ln=True)
            
            pdf.set_font("Arial", "", 11)
            f = t_info["filiacion"]
            pdf.cell(50, 7, "Apellido y Nombres:", 1, 0); pdf.cell(0, 7, limpiar_texto_pdf(f['nombre']), 1, 1)
            pdf.cell(50, 7, "D.N.I. / Sexo:", 1, 0); pdf.cell(0, 7, limpiar_texto_pdf(f"{f['dni']} | {f['sexo']}"), 1, 1)
            pdf.cell(50, 7, "F. Nacimiento:", 1, 0); pdf.cell(0, 7, limpiar_texto_pdf(f['fecha_nacimiento']), 1, 1)
            pdf.cell(50, 7, "Nacionalidad / E. Civil:", 1, 0); pdf.cell(0, 7, limpiar_texto_pdf(f"{f['nacionalidad']} | {f['estado_civil']}"), 1, 1)
            pdf.cell(50, 7, "Ocupacion:", 1, 0); pdf.cell(0, 7, limpiar_texto_pdf(f"{f['ocupacion']}"), 1, 1)
            pdf.cell(50, 7, "Contacto:", 1, 0); pdf.cell(0, 7, limpiar_texto_pdf(f"{f['telefono']} | {f['correo']}"), 1, 1)
            pdf.multi_cell(0, 7, limpiar_texto_pdf(f"Domicilio Real: {f['domicilio']}"), 1)
            pdf.ln(8)

            # RELATO
            pdf.set_font("Arial", "B", 11)
            pdf.cell(0, 8, "II. RELATO DE LA ENTREVISTA:", ln=True)
            pdf.set_font("Arial", "", 11)
            contenido = limpiar_texto_pdf(t_info["contenido"])
            pdf.multi_cell(0, 10, contenido if contenido else "SIN DECLARACION REGISTRADA", 0, 'J')

            # FIRMAS
            if pdf.get_y() > 240: pdf.add_page(); pdf.ln(20)
            else: pdf.ln(30)
            pdf.cell(90, 8, "------------------------------------", 0, 0, "C")
            pdf.cell(90, 8, "------------------------------------", 0, 1, "C")
            pdf.cell(90, 6, "FIRMA ENTREVISTADO", 0, 0, "C")
            pdf.cell(90, 6, "FIRMA INTERVINIENTE", 0, 1, "C")

    return pdf.output(dest="S").encode("latin-1", errors="replace") if hay_actas else None

def main():
    st.title("🚓 S.I.V. - Bloque 4: GESTIÓN DE TESTIGOS")
    st.caption("Autor: Sub Comisario CASTAÑEDA Juan")
    st.markdown("---")

    if "lista_testigos" not in st.session_state:
        st.session_state.lista_testigos = [1]

    datos_acumulados = {}

    for t_num in st.session_state.lista_testigos:
        with st.expander(f"🆔 {t_num}. DATOS FILIATORIOS DEL TESTIGO", expanded=True):
            c1, c2, c3 = st.columns([2, 1, 1])
            nombre = c1.text_input("Apellido y Nombres", key=f"n_{t_num}").upper()
            dni = c2.text_input("DNI", key=f"d_{t_num}")
            sexo = c3.selectbox("Sexo", ["MASCULINO", "FEMENINO", "OTRO"], key=f"s_{t_num}")

            c4, c5, c6 = st.columns([1, 1, 1])
            nacionalidad = c4.text_input("Nacionalidad", value="ARGENTINA", key=f"na_{t_num}").upper()
            estado_civil = c5.selectbox("Estado Civil", ["SOLTERO/A", "CASADO/A", "DIVORCIADO/A", "VIUDO/A", "CONCUBINO/A"], key=f"ec_{t_num}")
            
            # CORRECCIÓN: Formato AR y sin límites de año
            fecha_nacimiento = c6.date_input(
                "Fecha de Nacimiento",
                value=None,
                min_value=datetime(1920, 1, 1),
                max_value=datetime.now(),
                format="DD/MM/YYYY",
                key=f"fn_{t_num}"
            )

            c7, c8, c9 = st.columns([1, 1, 1])
            ocupacion = c7.text_input("Ocupación", key=f"oc_{t_num}").upper()
            telefono = c8.text_input("Teléfono Celular", key=f"te_{t_num}")
            correo = c9.text_input("Correo Electrónico", key=f"ma_{t_num}")
            domicilio = st.text_input("Domicilio Real", key=f"do_{t_num}").upper()

        st.subheader(f"✍️ {t_num}. Relato del Testigo")
        declara = st.radio(f"¿El testigo {t_num} presta declaración?", ["NO", "SI"], key=f"dec_{t_num}", horizontal=True)

        relato_final = ""
        if declara == "SI":
            relato_espontaneo = st.text_area("Relato del hecho:", key=f"re_{t_num}", height=120)
            if st.button(f"✨ Pulir Relato T{t_num}", key=f"pulir_{t_num}"):
                texto_pulido = (
                    "QUE EN LA FECHA, MANIFIESTA QUE: "
                    f"{relato_espontaneo.upper()}. "
                    "SE OBSERVA EL DESMONTE DE PERNOS Y BISAGRAS MEDIANTE EL USO DE HERRAMIENTAS, "
                    "ACCIÓN DIRIGIDA AL DESPRENDIMIENTO Y APODERAMIENTO DE LA PIEZA DE BRONCE, "
                    "VENCIENDO LA SEGURIDAD MECÁNICA DEL ELEMENTO."
                )
                st.session_state[f"ia_out_{t_num}"] = texto_pulido

            relato_final = st.text_area("Relato Procesado:", value=st.session_state.get(f"ia_out_{t_num}", ""), key=f"rip_{t_num}", height=150)

        # Guardado de datos incluyendo la fecha formateada
        f_nac_str = fecha_nacimiento.strftime("%d/%m/%Y") if fecha_nacimiento else "S/D"
        datos_acumulados[f"testigo_{t_num}"] = {
            "filiacion": {
                "nombre": nombre, "dni": dni, "sexo": sexo,
                "nacionalidad": nacionalidad, "estado_civil": estado_civil,
                "fecha_nacimiento": f_nac_str, "ocupacion": ocupacion,
                "telefono": telefono, "correo": correo, "domicilio": domicilio
            },
            "declara": declara,
            "contenido": relato_final
        }

    # Controles dinámicos
    col_add, col_del = st.columns(2)
    if col_add.button("➕ AGREGAR TESTIGO"):
        st.session_state.lista_testigos.append(len(st.session_state.lista_testigos) + 1)
        st.rerun()
    if len(st.session_state.lista_testigos) > 1 and col_del.button("🗑️ QUITAR ÚLTIMO"):
        st.session_state.lista_testigos.pop()
        st.rerun()

    # DESCARGAS
    st.subheader("💾 Finalizar y Descargar")
    pdf_data = generar_pdf_bytes(datos_acumulados, interviniente, lugar, hora_hecho)
    
    cj1, cj2 = st.columns(2)
    with cj1:
        st.download_button("📥 JSON PARA ACTANTE", data=json.dumps(datos_acumulados, indent=4, ensure_ascii=False), 
                           file_name=f"testigos_{datetime.now().strftime('%d%m%Y')}.json", mime="application/json")
    with cj2:
        if pdf_data:
            st.download_button("📄 DESCARGAR ACTAS EN PDF", data=pdf_data, 
                               file_name=f"Actas_Testigos_{datetime.now().strftime('%H%M')}.pdf", mime="application/pdf")

if __name__ == "__main__":
    main()
# CONFIGURACIÓN DE PÁGINA
st.set_page_config(
    page_title="S.I.V. - Bloque 4: Gestión de Testigos",
    layout="wide"
)

# --- SIDEBAR ---
with st.sidebar:
    st.header("Oficial Interviniente")
    interviniente = st.text_input(
        "Rango y Nombre",
        value="SUB COMISARIO CASTAÑEDA JUAN",
        disabled=True
    )

    st.markdown("---")
    st.subheader("Lugar del Hecho")
    lugar = st.text_input(
        "Dirección",
        placeholder="EJ: CALLE SARMIENTO 3361, ZAVALLA"
    )

    st.subheader("Hora del Hecho")
    hora_hecho = st.text_input("HH:MM", placeholder="08:00")

def limpiar_texto_pdf(texto):
    """Limpia caracteres especiales para evitar errores en FPDF"""
    if texto is None:
        return ""
    
    # Mapeo de caracteres especiales a compatibles con Latin-1
    reemplazos = {
        "“": '"', "”": '"', "‘": "'", "’": "'",
        "–": "-", "—": "-", "…": "...", "°": "Nro.",
        "ñ": "n", "Ñ": "N", "á": "a", "é": "e", "í": "i", "ó": "o", "ú": "u",
        "Á": "A", "É": "E", "Í": "I", "Ó": "O", "Ú": "U"
    }

    texto = str(texto)
    for original, reemplazo in reemplazos.items():
        texto = texto.replace(original, reemplazo)
    
    return texto

def generar_pdf_bytes(datos_acumulados, interviniente, lugar, hora_hecho):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    fecha_actual = datetime.now().strftime("%d/%m/%Y")
    # Si el oficial no puso hora, usamos la actual
    hora_documento = hora_hecho if hora_hecho else datetime.now().strftime("%H:%M")
    
    hay_actas = False

    for t_id, t_info in datos_acumulados.items():
        if t_info["declara"] == "SI":
            hay_actas = True
            pdf.add_page()

            # Cabecera Técnica
            pdf.set_font("Arial", "B", 14)
            pdf.cell(0, 10, "ACTA DE ENTREVISTA TECNICA", ln=True, align="C")
            pdf.ln(4)

            pdf.set_font("Arial", "", 10)
            pdf.cell(0, 8, limpiar_texto_pdf(f"LUGAR: {lugar if lugar else 'S/D'} | FECHA: {fecha_actual} | HORA: {hora_documento}"), ln=True)
            pdf.cell(0, 8, limpiar_texto_pdf(f"INTERVINIENTE: {interviniente}"), ln=True)
            
            pdf.line(10, 38, 200, 38)
            pdf.ln(8)

            # Filiación
            f = t_info["filiacion"]
            pdf.set_font("Arial", "B", 11)
            pdf.cell(0, 8, limpiar_texto_pdf(f"DATOS DEL TESTIGO {t_id.replace('_', ' ').upper()}"), ln=True)
            
            pdf.set_font("Arial", "", 11)
            pdf.cell(0, 7, limpiar_texto_pdf(f"APELLIDO Y NOMBRES: {f['nombre']}"), ln=True)
            pdf.cell(0, 7, limpiar_texto_pdf(f"DNI: {f['dni']} | SEXO: {f['sexo']}"), ln=True)
            pdf.cell(0, 7, limpiar_texto_pdf(f"NACIONALIDAD: {f['nacionalidad']} | ESTADO CIVIL: {f['estado_civil']}"), ln=True)
            pdf.cell(0, 7, limpiar_texto_pdf(f"OCUPACION: {f['ocupacion']}"), ln=True)
            pdf.cell(0, 7, limpiar_texto_pdf(f"CONTACTO: {f['telefono']} | {f['correo']}"), ln=True)
            pdf.multi_cell(0, 7, limpiar_texto_pdf(f"DOMICILIO: {f['domicilio']}"))
            
            pdf.ln(5)

            # Contenido Judicial
            pdf.set_font("Arial", "B", 11)
            pdf.cell(0, 8, "RELATO DE LA ENTREVISTA:", ln=True)
            pdf.set_font("Arial", "", 11)
            contenido = limpiar_texto_pdf(t_info["contenido"])
            pdf.multi_cell(0, 7, contenido if contenido else "SIN DECLARACION REGISTRADA")

            # Espacio para Firmas
            pdf.ln(25)
            pdf.cell(90, 8, "------------------------------------", 0, 0, "C")
            pdf.cell(90, 8, "------------------------------------", 0, 1, "C")
            pdf.cell(90, 6, "FIRMA ENTREVISTADO", 0, 0, "C")
            pdf.cell(90, 6, "FIRMA INTERVINIENTE", 0, 1, "C")

    if not hay_actas:
        return None

    # Generación segura del stream de datos
    return pdf.output(dest="S").encode("latin-1", errors="replace")

def main():
    st.title("🚓 S.I.V. - Bloque 4: GESTIÓN DE TESTIGOS")
    st.caption("Autor: Sub Comisario CASTAÑEDA Juan")
    st.markdown("---")

    if "lista_testigos" not in st.session_state:
        st.session_state.lista_testigos = [1]

    datos_acumulados = {}

    for t_num in st.session_state.lista_testigos:
        with st.expander(f"🆔 {t_num}. DATOS FILIATORIOS DEL TESTIGO", expanded=True):
            c1, c2, c3 = st.columns([2, 1, 1])
            nombre = c1.text_input("Apellido y Nombres", key=f"n_{t_num}").upper()
            dni = c2.text_input("DNI", key=f"d_{t_num}")
            sexo = c3.selectbox("Sexo", ["MASCULINO", "FEMENINO", "OTRO"], key=f"s_{t_num}")

            c4, c5, c6 = st.columns([1, 1, 1])
            nacionalidad = c4.text_input("Nacionalidad", value="ARGENTINA", key=f"na_{t_num}").upper()
            estado_civil = c5.selectbox("Estado Civil", ["SOLTERO/A", "CASADO/A", "DIVORCIADO/A", "VIUDO/A", "CONCUBINO/A"], key=f"ec_{t_num}")
            fecha_nacimiento = c6.date_input("Fecha de Nacimiento", key=f"fn_{t_num}")

            c7, c8, c9 = st.columns([1, 1, 1])
            ocupacion = c7.text_input("Ocupación", key=f"oc_{t_num}").upper()
            telefono = c8.text_input("Teléfono Celular", key=f"te_{t_num}")
            correo = c9.text_input("Correo Electrónico", key=f"ma_{t_num}")

            domicilio = st.text_input("Domicilio Real", key=f"do_{t_num}").upper()

        st.subheader(f"✍️ {t_num}. Relato del Testigo")
        declara = st.radio(f"¿El testigo {t_num} presta declaración?", ["NO", "SI"], key=f"dec_{t_num}", horizontal=True)

        relato_final = ""
        if declara == "SI":
            relato_espontaneo = st.text_area("Relato del hecho:", key=f"re_{t_num}", height=120)

            if st.button(f"✨ Pulir Relato T{t_num}", key=f"pulir_{t_num}"):
                # Criterio técnico para el caso del cura/sagrario
                texto_pulido = (
                    "QUE EN LA FECHA, MANIFIESTA QUE: "
                    f"{relato_espontaneo.upper()}. "
                    "SE OBSERVA EL DESMONTE DE PERNOS Y BISAGRAS MEDIANTE EL USO DE HERRAMIENTAS, "
                    "ACCIÓN DIRIGIDA AL DESPRENDIMIENTO Y APODERAMIENTO DE LA PIEZA DE BRONCE, "
                    "VENCIENDO LA SEGURIDAD MECÁNICA DEL ELEMENTO."
                )
                st.session_state[f"ia_out_{t_num}"] = texto_pulido

            relato_final = st.text_area(
                "Relato Procesado (Formato Judicial):",
                value=st.session_state.get(f"ia_out_{t_num}", ""),
                key=f"rip_{t_num}",
                height=150
            )

        datos_acumulados[f"testigo_{t_num}"] = {
            "filiacion": {
                "nombre": nombre, "dni": dni, "sexo": sexo,
                "nacionalidad": nacionalidad, "estado_civil": estado_civil,
                "fecha_nacimiento": str(fecha_nacimiento), "ocupacion": ocupacion,
                "telefono": telefono, "correo": correo, "domicilio": domicilio
            },
            "declara": declara,
            "contenido": relato_final
        }
        st.markdown("---")

    # Controles de cantidad de testigos
    col_add, col_del = st.columns(2)
    if col_add.button("➕ AGREGAR TESTIGO"):
        st.session_state.lista_testigos.append(len(st.session_state.lista_testigos) + 1)
        st.rerun()
    if len(st.session_state.lista_testigos) > 1:
        if col_del.button("🗑️ QUITAR ÚLTIMO"):
            st.session_state.lista_testigos.pop()
            st.rerun()

    # SECCIÓN DE DESCARGAS
    st.subheader("💾 Finalizar y Descargar")
    
    cj1, cj2 = st.columns(2)
    
    # 1. JSON (Data cruda)
    json_final = json.dumps(datos_acumulados, indent=4, ensure_ascii=False)
    cj1.download_button(
        "📥 DESCARGAR JSON PARA ACTANTE",
        data=json_final,
        file_name=f"testigos_{datetime.now().strftime('%d%m%Y_%H%M')}.json",
        mime="application/json"
    )

    # 2. PDF (Documento Judicial)
    pdf_data = generar_pdf_bytes(datos_acumulados, interviniente, lugar, hora_hecho)
    if pdf_data:
        cj2.download_button(
            label="📄 DESCARGAR ACTAS EN PDF",
            data=pdf_data,
            file_name=f"actas_SIV_{datetime.now().strftime('%d%m%Y_%H%M')}.pdf",
            mime="application/pdf"
        )
    else:
        cj2.button("📄 PDF (Sin declaraciones)", disabled=True)

if __name__ == "__main__":
    main()
