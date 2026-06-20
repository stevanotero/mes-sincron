from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException


async def manejador_errores_validacion(request: Request, exc: RequestValidationError):
    errores = []

    for error in exc.errors():
        campo = error.get("loc", [])
        campo_nombre = campo[-1] if campo else "desconocido"
        mensaje = error.get("msg", "Error de validación")

        # Limpiar el prefijo técnico "Value error, " que agrega Pydantic
        if mensaje.startswith("Value error, "):
            mensaje = mensaje.replace("Value error, ", "")

        errores.append({
            "campo": campo_nombre,
            "mensaje": mensaje
        })

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "exito": False,
            "mensaje": "Error de validación en los datos enviados",
            "errores": errores
        }
    )


async def manejador_errores_http(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "exito": False,
            "mensaje": exc.detail
        }
    )


async def manejador_errores_generales(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "exito": False,
            "mensaje": "Ocurrió un error interno en el servidor",
            "detalle": str(exc)
        }
    )