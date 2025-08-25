import sqlite3
import os

DB_NAME = "arca_de_jehova.db"

def crear_tablas():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # ---------------------------
    # Tabla Colonias
    # ---------------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS colonias (
            id_colonia INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_colonia VARCHAR(100) NOT NULL
        )
    """)

    # ---------------------------
    # Tabla Personas
    # ---------------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS personas (
            id_persona INTEGER PRIMARY KEY AUTOINCREMENT,
            nombres VARCHAR(100) NOT NULL,
            apellidos VARCHAR(100) NOT NULL,
            telefono VARCHAR(20),
            colonia_id INTEGER,
            foto_path VARCHAR(255) DEFAULT 'fotos/default.jpg',
            es_lider INTEGER DEFAULT 0,
            FOREIGN KEY (colonia_id) REFERENCES colonias(id_colonia)
                ON UPDATE CASCADE
                ON DELETE SET NULL
        )
    """)

    # ---------------------------
    # Tabla Casas de Paz
    # ---------------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS casas_paz (
            id_casa INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre VARCHAR(100) NOT NULL,
            direccion VARCHAR(200) NOT NULL,
            lider_id INTEGER,
            colonia_id INTEGER,
            FOREIGN KEY (lider_id) REFERENCES personas(id_persona)
                ON UPDATE CASCADE
                ON DELETE SET NULL,
            FOREIGN KEY (colonia_id) REFERENCES colonias(id_colonia)
                ON UPDATE CASCADE
                ON DELETE SET NULL
        )
    """)

    # ---------------------------
    # Tabla Eventos
    # ---------------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS eventos (
            id_evento INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo VARCHAR(150) NOT NULL,
            descripcion TEXT,
            fecha DATE NOT NULL,
            casa_id INTEGER,
            FOREIGN KEY (casa_id) REFERENCES casas_paz(id_casa)
                ON UPDATE CASCADE
                ON DELETE CASCADE
        )
    """)

    conn.commit()
    conn.close()
    print("✅ Tablas principales creadas correctamente (sin usuarios).")

if __name__ == "__main__":
    os.makedirs("fotos", exist_ok=True)
    crear_tablas()
