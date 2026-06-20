from pydantic import BaseModel

class LineaProduccion(BaseModel):
    nombre_linea: str
    capacidad_teorica: int
    tiempo_planificado: int
    tiempo_paradas: int
    unidades_producidas: int
    unidades_defectuosas: int
    estado: str