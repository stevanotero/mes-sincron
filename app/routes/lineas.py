from fastapi import APIRouter
from app.db import get_connection
from app.models import LineaProduccion

router = APIRouter()


@router.post("/")
def crear_linea(linea: LineaProduccion):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO lineas_produccion(
            nombre_linea,
            capacidad_teorica,
            tiempo_planificado,
            tiempo_paradas,
            unidades_producidas,
            unidades_defectuosas,
            estado,
            usuario_creador
        )
        VALUES(%s,%s,%s,%s,%s,%s,%s,%s)
        RETURNING id
    """, (
        linea.nombre_linea,
        linea.capacidad_teorica,
        linea.tiempo_planificado,
        linea.tiempo_paradas,
        linea.unidades_producidas,
        linea.unidades_defectuosas,
        linea.estado,
        1
    ))

    nuevo_id = cursor.fetchone()[0]

    conn.commit()

    cursor.close()
    conn.close()

    return {
        "mensaje": "Linea creada",
        "id": nuevo_id
    }


@router.get("/")
def listar_lineas():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            nombre_linea,
            capacidad_teorica,
            tiempo_planificado,
            tiempo_paradas,
            unidades_producidas,
            unidades_defectuosas,
            estado
        FROM lineas_produccion
    """)

    filas = cursor.fetchall()

    resultado = []

    for fila in filas:

        tiempo_operativo = fila[3] - fila[4]

        disponibilidad = (
            tiempo_operativo / fila[3]
            if fila[3] > 0 else 0
        )

        rendimiento = (
            fila[5] / (tiempo_operativo * fila[2])
            if tiempo_operativo > 0 and fila[2] > 0
            else 0
        )

        calidad = (
            (fila[5] - fila[6]) / fila[5]
            if fila[5] > 0
            else 0
        )

        oee = disponibilidad * rendimiento * calidad

        oee_porcentaje = round(oee * 100, 2)

        if oee_porcentaje < 65:
            clasificacion = "Inaceptable"
        elif oee_porcentaje < 75:
            clasificacion = "Regular"
        elif oee_porcentaje < 85:
            clasificacion = "Aceptable"
        elif oee_porcentaje < 95:
            clasificacion = "Buena"
        else:
            clasificacion = "Excelencia"

        resultado.append({
            "id": fila[0],
            "nombre_linea": fila[1],
            "estado": fila[7],
            "tiempo_operativo": tiempo_operativo,
            "disponibilidad": round(disponibilidad * 100, 2),
            "rendimiento": round(rendimiento * 100, 2),
            "calidad": round(calidad * 100, 2),
            "oee": oee_porcentaje,
            "clasificacion": clasificacion
        })

    cursor.close()
    conn.close()

    return resultado