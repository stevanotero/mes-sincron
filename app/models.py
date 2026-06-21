from pydantic import BaseModel, field_validator, model_validator
from typing import Literal


class LineaProduccion(BaseModel):
    nombre_linea: str
    capacidad_teorica: int
    tiempo_planificado: int
    tiempo_paradas: int
    unidades_producidas: int
    unidades_defectuosas: int
    estado: Literal["Activa", "Inactiva", "En Mantenimiento"]
   

    @field_validator("nombre_linea")
    @classmethod
    def nombre_no_vacio(cls, valor):
        if not valor or not valor.strip():
            raise ValueError("El nombre de la línea no puede estar vacío")
        return valor.strip()

    @field_validator("capacidad_teorica")
    @classmethod
    def capacidad_positiva(cls, valor):
        if valor <= 0:
            raise ValueError("La capacidad teórica debe ser mayor que 0")
        return valor

    @field_validator("tiempo_planificado")
    @classmethod
    def tiempo_planificado_positivo(cls, valor):
        if valor <= 0:
            raise ValueError("El tiempo planificado debe ser mayor que 0")
        return valor

    @field_validator("tiempo_paradas")
    @classmethod
    def tiempo_paradas_no_negativo(cls, valor):
        if valor < 0:
            raise ValueError("El tiempo de paradas no puede ser negativo")
        return valor

    @field_validator("unidades_producidas")
    @classmethod
    def unidades_producidas_no_negativas(cls, valor):
        if valor < 0:
            raise ValueError("Las unidades producidas no pueden ser negativas")
        return valor

    @field_validator("unidades_defectuosas")
    @classmethod
    def unidades_defectuosas_no_negativas(cls, valor):
        if valor < 0:
            raise ValueError("Las unidades defectuosas no pueden ser negativas")
        return valor

    @model_validator(mode="after")
    def validar_relaciones(self):
        if self.tiempo_paradas > self.tiempo_planificado:
            raise ValueError("El tiempo de paradas no puede ser mayor que el tiempo planificado")

        if self.unidades_defectuosas > self.unidades_producidas:
            raise ValueError("Las unidades defectuosas no pueden ser mayores que las unidades producidas")

        return self