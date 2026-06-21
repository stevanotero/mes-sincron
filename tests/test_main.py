from fastapi.testclient import TestClient
from app.main import app

cliente = TestClient(app)


def obtener_token():
    respuesta = cliente.post(
        "/api/auth/login",
        json={"username": "admin", "password": "admin123"}
    )
    return respuesta.json()["access_token"]


def test_login_correcto():
    respuesta = cliente.post(
        "/api/auth/login",
        json={"username": "admin", "password": "admin123"}
    )
    assert respuesta.status_code == 200
    assert "access_token" in respuesta.json()


def test_login_incorrecto():
    respuesta = cliente.post(
        "/api/auth/login",
        json={"username": "admin", "password": "claveincorrecta"}
    )
    assert respuesta.status_code == 401


def test_listar_lineas_sin_token():
    respuesta = cliente.get("/api/lineas/")
    assert respuesta.status_code == 401


def test_listar_lineas_con_token():
    token = obtener_token()
    respuesta = cliente.get(
        "/api/lineas/",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert respuesta.status_code == 200
    assert isinstance(respuesta.json(), list)


def test_crear_linea_datos_invalidos():
    token = obtener_token()
    respuesta = cliente.post(
        "/api/lineas/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "nombre_linea": "",
            "capacidad_teorica": -5,
            "tiempo_planificado": 480,
            "tiempo_paradas": 600,
            "unidades_producidas": 100,
            "unidades_defectuosas": 200,
            "estado": "Funcionando"
        }
    )
    assert respuesta.status_code == 422


def test_crud_completo_linea():
    token = obtener_token()
    headers = {"Authorization": f"Bearer {token}"}

    # Crear
    respuesta_crear = cliente.post(
        "/api/lineas/",
        headers=headers,
        json={
            "nombre_linea": "Linea Test Automatizado",
            "capacidad_teorica": 10,
            "tiempo_planificado": 480,
            "tiempo_paradas": 40,
            "unidades_producidas": 4000,
            "unidades_defectuosas": 120,
            "estado": "Activa"
        }
    )
    assert respuesta_crear.status_code == 200
    id_creado = respuesta_crear.json()["id"]

    # Obtener
    respuesta_obtener = cliente.get(f"/api/lineas/{id_creado}", headers=headers)
    assert respuesta_obtener.status_code == 200
    assert respuesta_obtener.json()["nombre_linea"] == "Linea Test Automatizado"

    # Actualizar
    respuesta_actualizar = cliente.put(
        f"/api/lineas/{id_creado}",
        headers=headers,
        json={
            "nombre_linea": "Linea Test Actualizada",
            "capacidad_teorica": 10,
            "tiempo_planificado": 480,
            "tiempo_paradas": 30,
            "unidades_producidas": 4200,
            "unidades_defectuosas": 100,
            "estado": "Activa"
        }
    )
    assert respuesta_actualizar.status_code == 200

    # Eliminar
    respuesta_eliminar = cliente.delete(f"/api/lineas/{id_creado}", headers=headers)
    assert respuesta_eliminar.status_code == 200

    # Confirmar que ya no existe
    respuesta_verificar = cliente.get(f"/api/lineas/{id_creado}", headers=headers)
    assert respuesta_verificar.status_code == 404