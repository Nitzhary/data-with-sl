-- =========================
-- TABLA DE PERSONAS
-- =========================
CREATE TABLE IF NOT EXISTS personas (
    id_persona INTEGER PRIMARY KEY AUTOINCREMENT,
    nombres VARCHAR(100) NOT NULL,
    apellidos VARCHAR(100) NOT NULL,
    telefono VARCHAR(20), -- opcional
    colonia VARCHAR(100), -- opcional
    foto VARCHAR(255) DEFAULT 'default.jpg'
);

-- =========================
-- TABLA DE CASAS DE PAZ
-- =========================
CREATE TABLE IF NOT EXISTS casas_paz (
    id_casa INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR(100) NOT NULL,
    direccion VARCHAR(200) NOT NULL,
    id_lider INTEGER,
    FOREIGN KEY (id_lider) REFERENCES personas(id_persona)
        ON UPDATE CASCADE
        ON DELETE SET NULL
);

-- =========================
-- TABLA DE EVENTOS
-- =========================
CREATE TABLE IF NOT EXISTS eventos (
    id_evento INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo VARCHAR(150) NOT NULL,
    descripcion TEXT,
    fecha DATE NOT NULL,
    id_casa INTEGER,
    FOREIGN KEY (id_casa) REFERENCES casas_paz(id_casa)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

-- =========================
-- TABLA DE PARTICIPANTES POR EVENTO
-- (para registrar quién asistió a qué evento)
-- =========================
CREATE TABLE IF NOT EXISTS evento_participantes (
    id_evento INTEGER,
    id_persona INTEGER,
    PRIMARY KEY (id_evento, id_persona),
    FOREIGN KEY (id_evento) REFERENCES eventos(id_evento)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY (id_persona) REFERENCES personas(id_persona)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);
