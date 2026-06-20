from fastapi import APIRouter, HTTPException, Depends
from app.db import get_connection
from app.models import LineaProduccion
from app.auth import obtener_usuario_actual

router = APIRouter()


@router.post("/")
def crear_linea(linea: LineaProduccion, usuario: dict = Depends(obtener_usuario_actual)):
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
        VALUES(%s, %s, %s, %s, %s, %s, %s, %s)
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
        "mensaje": "Línea creada exitosamente",
        "id": nuevo_id
    }


@router.get("/")
def listar_lineas(usuario: dict = Depends(obtener_usuario_actual)):
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

        disponibilidad = (tiempo_operativo / fila[3]) if fila[3] > 0 else 0
        rendimiento = (fila[5] / (tiempo_operativo * fila[2])) if tiempo_operativo > 0 and fila[2] > 0 else 0
        calidad = ((fila[5] - fila[6]) / fila[5]) if fila[5] > 0 else 0

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


@router.get("/{id}")
def obtener_linea(id: int, usuario: dict = Depends(obtener_usuario_actual)):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, nombre_linea, capacidad_teorica, tiempo_planificado, 
               tiempo_paradas, unidades_producidas, unidades_defectuosas, estado
        FROM lineas_produccion 
        WHERE id = %s
    """, (id,))

    fila = cursor.fetchone()
    cursor.close()
    conn.close()

    if not fila:
        raise HTTPException(status_code=404, detail="Línea no encontrada")

    return {
        "id": fila[0],
        "nombre_linea": fila[1],
        "capacidad_teorica": fila[2],
        "tiempo_planificado": fila[3],
        "tiempo_paradas": fila[4],
        "unidades_producidas": fila[5],
        "unidades_defectuosas": fila[6],
        "estado": fila[7]
    }


@router.put("/{id}")
def actualizar_linea(id: int, linea: LineaProduccion, usuario: dict = Depends(obtener_usuario_actual)):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE lineas_produccion
        SET nombre_linea = %s,
            capacidad_teorica = %s,
            tiempo_planificado = %s,
            tiempo_paradas = %s,
            unidades_producidas = %s,
            unidades_defectuosas = %s,
            estado = %s
        WHERE id = %s
        RETURNING id
    """, (
        linea.nombre_linea,
        linea.capacidad_teorica,
        linea.tiempo_planificado,
        linea.tiempo_paradas,
        linea.unidades_producidas,
        linea.unidades_defectuosas,
        linea.estado,
        id
    ))

    resultado = cursor.fetchone()
    conn.commit()
    cursor.close()
    conn.close()

    if not resultado:
        raise HTTPException(status_code=404, detail="Línea no encontrada")

    return {"mensaje": "Línea actualizada exitosamente", "id": id}


@router.delete("/{id}")
def eliminar_linea(id: int, usuario: dict = Depends(obtener_usuario_actual)):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM lineas_produccion WHERE id = %s RETURNING id", (id,))
    resultado = cursor.fetchone()
    conn.commit()
    cursor.close()
    conn.close()

    if not resultado:
        raise HTTPException(status_code=404, detail="Línea no encontrada")

    return {"mensaje": "Línea eliminada exitosamente", "id": id}