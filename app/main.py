from fastapi import FastAPI
from app.db import get_connection
from app.routes.lineas import router as lineas_router
from app.routes.auth import router as auth_router

app = FastAPI(
    title="Micro MES",
    version="1.0"
)

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