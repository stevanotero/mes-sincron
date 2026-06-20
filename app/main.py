from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.db import get_connection
from app.routes.lineas import router as lineas_router
from app.routes.auth import router as auth_router
from app.error_handlers import (
    manejador_errores_validacion,
    manejador_errores_http,
    manejador_errores_generales
)

app = FastAPI(
    title="Micro MES",
    version="1.0"
)

# Registrar manejadores de errores
app.add_exception_handler(RequestValidationError, manejador_errores_validacion)
app.add_exception_handler(StarletteHTTPException, manejador_errores_http)
app.add_exception_handler(Exception, manejador_errores_generales)


@app.get("/")
def home():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("SELECT version();")

    version = cursor.fetchone()

    cursor.close()
    conn.close()

    return {
        "mensaje": "Conexion exitosa",
        "postgres": version[0]
    }

app.include_router(auth_router)

app.include_router(
    lineas_router,
    prefix="/api/lineas",
    tags=["Lineas"]
)