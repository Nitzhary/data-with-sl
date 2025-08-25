import sqlite3
import hashlib
import os

DB_NAME = "arca_de_jehova.db"

# -------------------------------
# Función para hashear contraseñas
# -------------------------------
def hash_password(password: str) -> str:
    """Devuelve un hash SHA-256 de la contraseña."""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


# -------------------------------
# Crear tabla de usuarios
# -------------------------------
def crear_tabla_usuarios():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
            username VARCHAR(50) UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            rol VARCHAR(20) DEFAULT 'usuario'
        )
    """)

    conn.commit()
    conn.close()
    print("✅ Tabla de usuarios creada (si no existía).")


# -------------------------------
# Registro de usuarios
# -------------------------------
def registrar_usuario(username: str, password: str, rol: str = "usuario") -> bool:
    """Registra un nuevo usuario con contraseña hasheada."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO usuarios (username, password_hash, rol)
            VALUES (?, ?, ?)
        """, (username, hash_password(password), rol))
        conn.commit()
        print(f"✅ Usuario '{username}' registrado correctamente.")
        return True
    except sqlite3.IntegrityError:
        print(f"⚠️ El usuario '{username}' ya existe.")
        return False
    finally:
        conn.close()


# -------------------------------
# Verificación de login
# -------------------------------
def verificar_usuario(username: str, password: str) -> bool:
    """Verifica si el usuario y contraseña son correctos."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT password_hash FROM usuarios WHERE username = ?
    """, (username,))
    row = cursor.fetchone()
    conn.close()

    if row:
        stored_hash = row[0]
        return stored_hash == hash_password(password)
    return False


# -------------------------------
# Inicializador
# -------------------------------
if __name__ == "__main__":
    crear_tabla_usuarios()

    # Admin por defecto
    registrar_usuario("admin", "admin123", rol="admin")

    # Usuarios hardcodeados
    registrar_usuario("Sariely", "Hasbey", rol="usuario")
    registrar_usuario("Titanium", "Titanium", rol="admin")

    # Pruebas rápidas
    print("Login correcto (admin):", verificar_usuario("admin", "admin123"))
    print("Login correcto (Sariely):", verificar_usuario("Sariely", "Hasbey"))
    print("Login correcto (Titanium):", verificar_usuario("Titanium", "Titanium"))
    print("Login incorrecto:", verificar_usuario("admin", "wrongpass"))
