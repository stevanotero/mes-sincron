from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.config import JWT_SECRET, JWT_ALGORITHM
from app.db import get_connection

# Configuración
CLAVE_SECRETA = JWT_SECRET
ALGORITMO = JWT_ALGORITHM
MINUTOS_EXPIRACION_TOKEN = 60

contexto_password = CryptContext(schemes=["bcrypt"], deprecated="auto")
esquema_bearer = HTTPBearer()


def verificar_password(password_plano, password_hasheado):
    return contexto_password.verify(password_plano, password_hasheado)


def generar_hash_password(password):
    return contexto_password.hash(password)


def autenticar_usuario(username: str, password: str):
    """
    Busca el usuario en la base de datos y verifica su contraseña.
    Devuelve el usuario (id, username) si es válido, o None si no.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, username, password_hash FROM usuarios WHERE username = %s",
        (username,)
    )
    fila = cursor.fetchone()

    cursor.close()
    conn.close()

    if not fila:
        return None

    usuario_id, usuario_username, password_hash = fila

    if not verificar_password(password, password_hash):
        return None

    return {"id": usuario_id, "username": usuario_username}


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
        usuario_id: int = payload.get("id")
        if username is None or usuario_id is None:
            raise excepcion_credenciales
    except JWTError:
        raise excepcion_credenciales
    return {"id": usuario_id, "username": username}