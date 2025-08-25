import sqlite3
import os

DB_NAME = "arca_de_jehova.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

# ---------------------------
# CRUD Colonias
# ---------------------------
def agregar_colonia(nombre_colonia):
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT OR IGNORE INTO colonias (nombre_colonia) VALUES (?)", (nombre_colonia,))
    except Exception as e:
        print(f"❌ Error al agregar colonia: {e}")

def obtener_colonias():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM colonias ORDER BY nombre_colonia")
        return cursor.fetchall()

def eliminar_colonia(id_colonia):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM colonias WHERE id_colonia=?", (id_colonia,))

# ---------------------------
# CRUD Personas
# ---------------------------
def agregar_persona(id_persona, nombres, apellidos, telefono=None, colonia_id=None, foto_path=None, es_lider=0):
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            if id_persona:  
                cursor.execute("""
                    INSERT INTO personas (id_persona, nombres, apellidos, telefono, colonia_id, foto_path, es_lider)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (id_persona, nombres, apellidos, telefono, colonia_id, foto_path, es_lider))
            else:  
                cursor.execute("""
                    INSERT INTO personas (nombres, apellidos, telefono, colonia_id, foto_path, es_lider)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (nombres, apellidos, telefono, colonia_id, foto_path, es_lider))
    except Exception as e:
        print(f"❌ Error al agregar persona: {e}")

def obtener_personas():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM personas ORDER BY id_persona DESC")
        return cursor.fetchall()

def actualizar_persona(id_persona, nombres, apellidos, telefono=None, colonia_id=None, foto_path=None, es_lider=0):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE personas 
            SET nombres=?, apellidos=?, telefono=?, colonia_id=?, foto_path=?, es_lider=?
            WHERE id_persona=?
        """, (nombres, apellidos, telefono, colonia_id, foto_path, es_lider, id_persona))

def eliminar_persona(id_persona):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM personas WHERE id_persona=?", (id_persona,))

# ---------------------------
# CRUD Casas de Paz
# ---------------------------
def agregar_casa(direccion, lider_id=None, colonia_id=None, nombre="Casa de Paz"):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO casas_paz (nombre, direccion, lider_id, colonia_id)
            VALUES (?, ?, ?, ?)
        """, (nombre, direccion, lider_id, colonia_id))

def obtener_casas():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT c.id_casa, c.direccion, col.nombre_colonia, 
                   p.nombres || ' ' || p.apellidos AS lider
            FROM casas_paz c
            LEFT JOIN colonias col ON c.colonia_id = col.id_colonia
            LEFT JOIN personas p ON c.lider_id = p.id_persona
            ORDER BY c.id_casa DESC
        """)
        return cursor.fetchall()

def eliminar_casa(id_casa):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM casas_paz WHERE id_casa=?", (id_casa,))

# ---------------------------
# CRUD Eventos
# ---------------------------
def agregar_evento(titulo, fecha, descripcion=None, casa_id=None):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO eventos (titulo, fecha, descripcion, casa_id)
            VALUES (?, ?, ?, ?)
        """, (titulo, fecha, descripcion, casa_id))

def obtener_eventos():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT e.id_evento, e.titulo, e.fecha, e.descripcion, c.direccion
            FROM eventos e
            LEFT JOIN casas_paz c ON e.casa_id = c.id_casa
            ORDER BY e.fecha DESC
        """)
        return cursor.fetchall()

def eliminar_evento(id_evento):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM eventos WHERE id_evento=?", (id_evento,))

# ---------------------------
# CRUD Usuarios (para login)
# ---------------------------
def agregar_usuario(username, password_hash, role="user"):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR IGNORE INTO usuarios (username, password_hash, role)
            VALUES (?, ?, ?)
        """, (username, password_hash, role))

def obtener_usuario(username):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE username=?", (username,))
        return cursor.fetchone()
