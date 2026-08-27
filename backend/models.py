from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from enum import Enum


class NivelEducativo(str, Enum):
    BACHILLERATO = "Bachillerato"
    TECNICO = "Tecnico"
    UNIVERSITARIO = "Universitario"
    POSTGRADO = "Postgrado"


class CategoriaHabilidad(str, Enum):
    COGNITIVA = "Cognitiva"
    TECNICA = "Tecnica"
    BLANDA = "Blanda"
    ACADEMICA = "Academica"


class PersonaBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100)
    edad: int = Field(..., ge=14, le=100)
    nivel_educativo: NivelEducativo
    email: EmailStr


class PersonaCreate(PersonaBase):
    id: Optional[str] = None
    habilidades_ids: list[str] = Field(default_factory=list)


class PersonaResponse(PersonaBase):
    id: str
    habilidades: list[str] = Field(default_factory=list)

    class Config:
        from_attributes = True


class HabilidadBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100)
    categoria: CategoriaHabilidad


class HabilidadCreate(HabilidadBase):
    id: Optional[str] = None


class HabilidadResponse(HabilidadBase):
    id: str

    class Config:
        from_attributes = True


class CarreraBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=150)
    descripcion: str = Field(..., min_length=1, max_length=500)
    facultad: str = Field(..., min_length=1, max_length=100)


class CarreraCreate(CarreraBase):
    id: Optional[str] = None
    requiere: list[str] = Field(default_factory=list)


class CarreraResponse(CarreraBase):
    id: str
    requiere: list[str] = Field(default_factory=list)

    class Config:
        from_attributes = True


class CompatibilidadResponse(BaseModel):
    carrera: str
    coincidencias: int
    total_requeridas: int
    compatibilidad: float

    class Config:
        from_attributes = True


class CompatibilidadRequest(BaseModel):
    persona_id: str