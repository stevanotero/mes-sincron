from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.config import JWT_SECRET, JWT_ALGORITHM

# Configuración
CLAVE_SECRETA = JWT_SECRET
ALGORITMO = JWT_ALGORITHM
MINUTOS_EXPIRACION_TOKEN = 60

contexto_password = CryptContext(schemes=["bcrypt"], deprecated="auto")
esquema_bearer = HTTPBearer()

# Usuario de prueba (temporal, mientras no haya tabla de usuarios)
USUARIO_PRUEBA = {
    "username": "admin",
    "password": "",
    "nombre": "Administrador"
}

def verificar_password(password_plano, password_hasheado):
    return contexto_password.verify(password_plano, password_hasheado)

def generar_hash_password(password):
    return contexto_password.hash(password)

def crear_token_acceso(datos: dict, tiempo_expiracion: Optional[timedelta] = None):
    datos_codificar = datos.copy()
    if tiempo_expiracion:
        expira = datetime.utcnow() + tiempo_expiracion
    else:
        expira = datetime.utcnow() + timedelta(minutes=MINUTOS_EXPIRACION_TOKEN)
    datos_codificar.update({"exp": expira})
    token_jwt = jwt.encode(datos_codificar, CLAVE_SECRETA, algorithm=ALGORITMO)
    return token_jwt

async def obtener_usuario_actual(credenciales: HTTPAuthorizationCredentials = Depends(esquema_bearer)):
    excepcion_credenciales = HTTPException(
        status_code=401,
        detail="Credenciales inválidas",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token = credenciales.credentials
    try:
        payload = jwt.decode(token, CLAVE_SECRETA, algorithms=[ALGORITMO])
        username: str = payload.get("sub")
        if username is None:
            raise excepcion_credenciales
    except JWTError:
        raise excepcion_credenciales
    return {"username": username}