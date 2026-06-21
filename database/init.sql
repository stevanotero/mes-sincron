-- =========================================================
-- Script de inicialización - Micro MES
-- Base de datos: PostgreSQL
-- =========================================================

-- Tabla de usuarios (supervisores de planta)
CREATE TABLE IF NOT EXISTS usuarios (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de líneas de producción
CREATE TABLE IF NOT EXISTS lineas_produccion (
    id SERIAL PRIMARY KEY,
    nombre_linea VARCHAR(100) NOT NULL,
    capacidad_teorica INTEGER NOT NULL CHECK (capacidad_teorica > 0),
    tiempo_planificado INTEGER NOT NULL CHECK (tiempo_planificado > 0),
    tiempo_paradas INTEGER DEFAULT 0 CHECK (tiempo_paradas >= 0),
    unidades_producidas INTEGER DEFAULT 0 CHECK (unidades_producidas >= 0),
    unidades_defectuosas INTEGER DEFAULT 0 CHECK (unidades_defectuosas >= 0),
    estado VARCHAR(30) NOT NULL CHECK (estado IN ('Activa', 'Inactiva', 'En Mantenimiento')),
    usuario_creador INTEGER NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Índice para acelerar las búsquedas de líneas por supervisor
CREATE INDEX IF NOT EXISTS idx_lineas_usuario_creador 
    ON lineas_produccion(usuario_creador);

-- =========================================================
-- Usuario de prueba (supervisor inicial)
-- Username: admin
-- Password: admin123  (ya viene hasheada con bcrypt)
-- =========================================================
INSERT INTO usuarios (username, password_hash)
VALUES ('admin', '$2b$12$jG8vZqgRlJMSNk5Nb892f.Sk2hfigMy9uIa88LzIqht4AQ/qO3z1a')
ON CONFLICT (username) DO NOTHING;