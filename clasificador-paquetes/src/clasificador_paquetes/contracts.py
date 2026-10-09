from typing import Literal
from pydantic import BaseModel, ConfigDict, Field, field_validator


class Entrada(BaseModel):
    id_paquete: str = Field(min_length = 1)
    peso_kg: float = Field(ge = 1, le= 30)
    distancia_km : int = Field(ge = 0, le= 200)

    @field_validator("id_paquetes", mode="before", check_fields=False)
    @classmethod
    def id_paquete_validator(cls, value):
        return value.strip()


class Salida(BaseModel):
  
    id_paquete: str = Field(min_length = 1)
    categoria: Literal["normal", "urgente"]
    confianza: float = Field(ge = 0, le= 1)
