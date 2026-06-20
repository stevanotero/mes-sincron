from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.auth import verificar_password, crear_token_acceso, generar_hash_password, USUARIO_PRUEBA

router = APIRouter(prefix="/api/auth", tags=["Auth"])

class SolicitudLogin(BaseModel):
    username: str
    password: str

class RespuestaToken(BaseModel):
    access_token: str
    token_type: str = "bearer"

# Contraseña hasheada para "admin123"
USUARIO_PRUEBA["password"] = generar_hash_password("admin123")

@router.post("/login", response_model=RespuestaToken)
def login(credenciales: SolicitudLogin):
    if credenciales.username != USUARIO_PRUEBA["username"]:
        raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")

    if not verificar_password(credenciales.password, USUARIO_PRUEBA["password"]):
        raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")

    token_acceso = crear_token_acceso(datos={"sub": credenciales.username})

    return {
        "access_token": token_acceso,
        "token_type": "bearer"
    }