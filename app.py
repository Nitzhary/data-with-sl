import streamlit as st
import crud
import auth
import os
import sys
import sqlite3
from datetime import date
import subprocess
import webbrowser



# ===========================
# Mensaje de bienvenida en consola
# ===========================
print("===========================================")
print(" Bienvenido al programa Data Entry.        ")
print(" Gracias por utilizar mi programa          ")
print(" Released by GIDDIANI \"HARDCODE\" ©         ")
print("===========================================")


# ===========================
# Función para rutas seguras (para exe y normal)
# ===========================
def resource_path(relative_path: str) -> str:
    """Devuelve la ruta absoluta del recurso, incluso cuando está en .exe"""
    try:
        base_path = sys._MEIPASS  # carpeta temporal de PyInstaller
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


# ===========================
# Configuración de rutas
# ===========================
DB_PATH = resource_path("arca_de_jehova.db")
SCHEMA_PATH = resource_path("schema.sql")
FOTOS_PATH = resource_path("fotos")

# Crear la carpeta fotos si no existe
os.makedirs(FOTOS_PATH, exist_ok=True)

# Inicializar base de datos si no existe
if not os.path.exists(DB_PATH):
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        schema = f.read()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.executescript(schema)
    conn.commit()
    conn.close()


# ===========================
# Configuración de Streamlit
# ===========================
st.set_page_config(page_title="Data Entry - Iglesia Arca de Jehová", layout="wide")
st.title("📋 Data Entry - Iglesia Arca de Jehová")

st.success("Bienvenido al programa Data Entry 🎉")
st.info("Gracias por utilizar mi programa 🙌")
st.markdown("**Released by GIDDIANI 'HARDCODE' ©**")


# ===========================
# Estado de sesión
# ===========================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "usuario" not in st.session_state:
    st.session_state.usuario = None
if "active_tab" not in st.session_state:
    st.session_state["active_tab"] = 0  # 0 colonias, 1 personas, 2 casas, 3 eventos


def refresh(tab_index: int):
    st.session_state["active_tab"] = tab_index
    st.rerun()


# ===========================
# Pantalla de Login
# ===========================
if not st.session_state.logged_in:
    st.subheader("🔑 Inicio de sesión")

    with st.form("login_form"):
        username = st.text_input("Usuario", key="login_user")
        password = st.text_input("Contraseña", type="password", key="login_pass")
        login_btn = st.form_submit_button("Iniciar sesión")

        if login_btn:
            if auth.verificar_usuario(username, password):
                st.session_state.logged_in = True
                st.session_state.usuario = username
                st.success(f"✅ Bienvenido, {username}")
                st.rerun()
            else:
                st.error("❌ Usuario o contraseña incorrectos.")
    st.stop()  # 🔒 Detiene la ejecución si no hay login


# ===========================
# Menú superior 
# ===========================
col1, col2 = st.columns([8, 2])
with col1:
    st.write(f"👋 Bienvenido, **{st.session_state.usuario}**")
with col2:
    if st.button("🚪 Cerrar sesión", key="logout_btn"):
        st.session_state.logged_in = False
        st.session_state.usuario = None
        st.rerun()


# ===========================
# Pestañas 
# ===========================
tab_colonias, tab_personas, tab_casas, tab_eventos = st.tabs(
    ["🏘️ Colonias", "👤 Personas", "🏠 Casas de Paz", "📅 Eventos"]
)


# ===========================
# Colonias
# ===========================
with tab_colonias:
    st.header("🏘️ Colonias")

    with st.form("form_colonia", clear_on_submit=True):
        nombre = st.text_input("Nombre de la colonia", key="colonia_nombre_input")
        submit_colonia = st.form_submit_button("Agregar")
        if submit_colonia:
            if nombre.strip():
                crud.agregar_colonia(nombre.strip())
                st.success(f"✅ Colonia '{nombre}' registrada.")
                refresh(0)
            else:
                st.warning("⚠️ Ingresa un nombre válido.")

    st.subheader("Colonias registradas")
    colonias = crud.obtener_colonias()
    if colonias:
        for c in colonias:
            col1, col2 = st.columns([5, 1])
            with col1:
                col1.write(f"**{c[1]}**")
            with col2:
                if st.button("🗑️", key=f"colonia_btn_{c[0]}"):
                    crud.eliminar_colonia(c[0])
                    st.warning(f"Colonia '{c[1]}' eliminada.")
                    refresh(0)
    else:
        st.info("No hay colonias registradas.")


# ===========================
# Personas
# ===========================
with tab_personas:
    st.header("👤 Personas")

    colonias = crud.obtener_colonias()
    colonia_options = {c[1]: c[0] for c in colonias}  # {nombre: id}

    # IDs existentes para validar unicidad
    personas_existentes = crud.obtener_personas()
    ids_existentes = set([p[0] for p in personas_existentes])

    with st.form("form_persona", clear_on_submit=True):
        persona_id_str = st.text_input("ID (obligatorio, numérico y único)", key="persona_id_input")
        nombres = st.text_input("Nombres", key="persona_nombres_input")
        apellidos = st.text_input("Apellidos", key="persona_apellidos_input")
        telefono = st.text_input("Teléfono", key="persona_telefono_input")
        colonia_sel = st.selectbox("Colonia", list(colonia_options.keys()) if colonia_options else [], key="persona_colonia_select")
        es_lider = st.checkbox("¿Es líder?", key="persona_es_lider_check")
        foto = st.file_uploader("Foto", type=["jpg", "jpeg", "png"], key="persona_foto_uploader")
        submitted_persona = st.form_submit_button("Agregar")

        if submitted_persona:
            pid = None
            if not persona_id_str.strip():
                st.error("❌ El ID es obligatorio.")
            elif not persona_id_str.isdigit():
                st.error("❌ El ID debe ser numérico.")
            else:
                pid = int(persona_id_str)
                if pid in ids_existentes:
                    st.error(f"❌ El ID {pid} ya existe. Debe ser único.")
                    pid = None

            if pid is not None and nombres.strip() and apellidos.strip() and colonia_options:
                os.makedirs(FOTOS_PATH, exist_ok=True)
                foto_path = os.path.join(FOTOS_PATH, "default.jpg")
                if foto:
                    safe_name = foto.name.replace(" ", "_")
                    foto_path = os.path.join(FOTOS_PATH, f"{pid}_{safe_name}")
                    with open(foto_path, "wb") as f:
                        f.write(foto.getbuffer())

                try:
                    crud.agregar_persona(
                        pid, nombres.strip(), apellidos.strip(),
                        telefono=telefono.strip() or None,
                        colonia_id=colonia_options[colonia_sel],
                        foto_path=foto_path,
                        es_lider=1 if es_lider else 0,
                    )
                    st.success(f"✅ Persona {nombres} {apellidos} registrada.")
                    refresh(1)
                except Exception as e:
                    st.error(f"❌ No se pudo registrar la persona: {e}")
            else:
                if pid is not None and (not nombres.strip() or not apellidos.strip() or not colonia_options):
                    st.warning("⚠️ Nombres, apellidos y colonia son obligatorios.")

    st.subheader("Personas registradas")
    personas = crud.obtener_personas()
    if personas:
        for p in personas:
            pid, pnombres, papellidos, ptel, pcol_id, pfoto, plider = p
            col1, col2, col3, col4 = st.columns([1, 3, 4, 1])

            with col1:
                img_path = pfoto if (pfoto and os.path.exists(pfoto)) else os.path.join(FOTOS_PATH, "default.jpg")
                st.image(img_path, width=80)

            with col2:
                st.write(f"**ID:** {pid}")
                st.write(f"**Nombre:** {pnombres} {papellidos}")
                st.write(f"**Teléfono:** {ptel or 'No registrado'}")
                colonia_nombre = next((c[1] for c in colonias if c[0] == pcol_id), "Desconocida")
                st.write(f"**Colonia:** {colonia_nombre}")
                st.write(f"**¿Líder?:** {'Sí' if plider == 1 else 'No'}")

            with col3:
                with st.form(f"edit_{pid}", clear_on_submit=False):
                    nuevo_nombre = st.text_input("Nombres", value=pnombres, key=f"nom_{pid}")
                    nuevo_apellido = st.text_input("Apellidos", value=papellidos, key=f"ape_{pid}")
                    nuevo_tel = st.text_input("Teléfono", value=ptel or "", key=f"tel_{pid}")

                    colonias_nombres = list(colonia_options.keys())
                    try:
                        idx_col = list(colonia_options.values()).index(pcol_id) if pcol_id in colonia_options.values() else 0
                    except ValueError:
                        idx_col = 0

                    nueva_col = st.selectbox("Colonia", colonias_nombres, index=idx_col, key=f"col_persona_{pid}")
                    nuevo_lider = st.checkbox("¿Es líder?", value=(plider == 1), key=f"lider_{pid}")
                    nueva_foto = st.file_uploader("Foto nueva", type=["jpg", "jpeg", "png"], key=f"foto_{pid}")
                    submitted_edit = st.form_submit_button("Guardar")

                    if submitted_edit:
                        foto_final = pfoto
                        if nueva_foto:
                            os.makedirs(FOTOS_PATH, exist_ok=True)
                            safe_name = nueva_foto.name.replace(" ", "_")
                            foto_final = os.path.join(FOTOS_PATH, f"{pid}_{safe_name}")
                            with open(foto_final, "wb") as f:
                                f.write(nueva_foto.getbuffer())

                        try:
                            crud.actualizar_persona(
                                pid, nuevo_nombre.strip(), nuevo_apellido.strip(),
                                telefono=nuevo_tel.strip() or None,
                                colonia_id=colonia_options[nueva_col],
                                foto_path=foto_final,
                                es_lider=1 if nuevo_lider else 0,
                            )
                            st.success("✅ Persona actualizada.")
                            refresh(1)
                        except Exception as e:
                            st.error(f"❌ No se pudo actualizar la persona: {e}")

            with col4:
                if st.button("🗑️", key=f"del_persona_{pid}"):
                    try:
                        crud.eliminar_persona(pid)
                        st.warning(f"Persona {pnombres} {papellidos} eliminada.")
                        refresh(1)
                    except Exception as e:
                        st.error(f"❌ No se pudo eliminar: {e}")
    else:
        st.info("No hay personas registradas.")


# ===========================
# Casas de Paz
# ===========================
with tab_casas:
    st.header("🏠 Casas de Paz")

    personas = crud.obtener_personas()
    colonias = crud.obtener_colonias()
    casas = crud.obtener_casas()

    lideres = [p for p in personas if p[6] == 1]
    lider_options = {f"{p[1]} {p[2]} (ID {p[0]})": p[0] for p in lideres}
    colonia_options_casa = {c[1]: c[0] for c in colonias}

    with st.form("form_casa", clear_on_submit=True):
        direccion = st.text_input("Dirección", key="casa_direccion_input")
        lider_sel = st.selectbox("Líder (solo líderes)", ["Ninguno"] + list(lider_options.keys()), key="casa_lider_select")
        colonia_sel = st.selectbox("Colonia", ["Ninguna"] + list(colonia_options_casa.keys()), key="casa_colonia_select")
        submitted_casa = st.form_submit_button("Agregar")

        if submitted_casa:
            if direccion.strip():
                lider_id = None if lider_sel == "Ninguno" else lider_options[lider_sel]
                colonia_id = None if colonia_sel == "Ninguna" else colonia_options_casa[colonia_sel]
                try:
                    crud.agregar_casa(direccion.strip(), lider_id, colonia_id)
                    st.success("✅ Casa registrada.")
                    refresh(2)
                except Exception as e:
                    st.error(f"❌ No se pudo registrar la casa: {e}")
            else:
                st.warning("⚠️ Ingresa la dirección.")

    st.subheader("Casas registradas")
    if casas:
        for c in casas:
            col1, col2 = st.columns([5, 1])
            with col1:
                col1.write(f"**Dirección:** {c[1]}  |  **Colonia:** {c[2] or 'Sin colonia'}  |  **Líder:** {c[3] or 'Sin líder'}")
            with col2:
                if st.button("🗑️", key=f"casa_btn_{c[0]}"):
                    try:
                        crud.eliminar_casa(c[0])
                        st.warning("Casa eliminada.")
                        refresh(2)
                    except Exception as e:
                        st.error(f"❌ No se pudo eliminar la casa: {e}")
    else:
        st.info("No hay casas registradas.")


# ===========================
# Eventos
# ===========================
with tab_eventos:
    st.header("📅 Eventos")

    casas = crud.obtener_casas()
    eventos = crud.obtener_eventos()
    casa_options_ev = {c[1]: c[0] for c in casas}

    with st.form("form_evento", clear_on_submit=True):
        titulo = st.text_input("Título", key="evento_titulo_input")
        descripcion = st.text_area("Descripción", key="evento_desc_input")
        fecha_ev = st.date_input("Fecha", value=date.today(), key="evento_fecha_input")
        casa_sel = st.selectbox("Casa", ["Ninguna"] + list(casa_options_ev.keys()), key="evento_casa_select")
        submitted_evento = st.form_submit_button("Agregar")

        if submitted_evento:
            if titulo.strip():
                casa_id = None if casa_sel == "Ninguna" else casa_options_ev[casa_sel]
                try:
                    crud.agregar_evento(titulo.strip(), fecha_ev, descripcion.strip() if descripcion else None, casa_id)
                    st.success("✅ Evento registrado.")
                    refresh(3)
                except Exception as e:
                    st.error(f"❌ No se pudo registrar el evento: {e}")
            else:
                st.warning("⚠️ Ingresa un título.")

    st.subheader("Eventos registrados")
    if eventos:
        for e in eventos:
            col1, col2, col3, col4, col5 = st.columns([2, 2, 3, 3, 1])
            with col1:
                col1.write(f"**{e[1]}**")
            with col2:
                col2.write(str(e[2]))
            with col3:
                col3.write(e[3] or "Sin descripción")
            with col4:
                col4.write(e[4] or "Sin casa")
            with col5:
                if st.button("🗑️", key=f"ev_btn_{e[0]}"):
                    try:
                        crud.eliminar_evento(e[0])
                        st.warning("Evento eliminado.")
                        refresh(3)
                    except Exception as e:
                        st.error(f"❌ No se pudo eliminar: {e}")
    else:
        st.info("No hay eventos registrados.")


# ===========================
# Footer
# ===========================
footer = """
    <style>
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        text-align: center;
        font-size: 12px;
        color: gray;
        padding: 5px;
    }
    </style>
    <div class="footer">
        Released by GIDDIANI ©
    </div>
"""
st.markdown(footer, unsafe_allow_html=True)
