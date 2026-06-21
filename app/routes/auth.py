from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.auth import autenticar_usuario, crear_token_acceso

router = APIRouter(prefix="/api/auth", tags=["Auth"])


class SolicitudLogin(BaseModel):
    username: str
    password: str


class RespuestaToken(BaseModel):
    access_token: str
    token_type: str = "bearer"


@router.post("/login", response_model=RespuestaToken)
def login(credenciales: SolicitudLogin):
    usuario = autenticar_usuario(credenciales.username, credenciales.password)

    if not usuario:
        raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")

    token_acceso = crear_token_acceso(
        datos={"sub": usuario["username"], "id": usuario["id"]}
    )

    return {
        "access_token": token_acceso,
        "token_type": "bearer"
    }