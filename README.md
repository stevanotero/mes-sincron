# Sistema MES - Sincrón Diseño Electrónico

Sistema de Manufacturing Execution System (MES) desarrollado con FastAPI y PostgreSQL para el monitoreo en tiempo real de líneas de producción y cálculo de OEE.

## Tecnologías utilizadas

- Backend: FastAPI + Uvicorn
- Base de datos: PostgreSQL
- ORM: SQLAlchemy
- Validaciones: Pydantic
- Documentación: Swagger UI

## Funcionalidades implementadas

- CRUD completo de líneas de producción
- Cálculo automático de OEE (Disponibilidad, Rendimiento, Calidad y Clasificación)
- Conexión con PostgreSQL

## Endpoints principales

| Método | Endpoint               | Descripción                    |
|--------|------------------------|--------------------------------|
| POST   | /api/lineas/           | Crear nueva línea              |
| GET    | /api/lineas/           | Listar todas las líneas        |
| GET    | /api/lineas/{id}       | Obtener una línea              |
| PUT    | /api/lineas/{id}       | Actualizar línea               |
| DELETE | /api/lineas/{id}       | Eliminar línea                 |

## Cómo ejecutar el proyecto

1. Clonar el repositorio
```bash
git clone https://github.com/stevanotero/mes-sincron.git
cd mes-sincron