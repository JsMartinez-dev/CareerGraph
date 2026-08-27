from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import List

from backend.config import settings
from backend.database import get_driver, close_driver
from backend.crud import (
    obtener_personas, obtener_persona, crear_persona, actualizar_persona, eliminar_persona,
    obtener_carreras, obtener_carrera, crear_carrera,
    obtener_habilidades, obtener_habilidad, crear_habilidad,
    obtener_compatibilidad, obtener_estadisticas
)
from backend.models import (
    PersonaCreate, PersonaResponse,
    CarreraCreate, CarreraResponse,
    HabilidadCreate, HabilidadResponse,
    CompatibilidadResponse
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    get_driver()  # Initialize driver lazily
    yield
    close_driver()


app = FastAPI(
    title="CareerGraph API",
    description="API para recomendación de carreras basada en grafos (Neo4j)",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "CareerGraph API", "version": "1.0.0"}


@app.get("/health")
def health_check():
    try:
        driver = get_driver()
        driver.verify_connectivity()
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Database unavailable: {str(e)}")


@app.get("/stats")
def get_stats():
    return obtener_estadisticas()


# Personas endpoints
@app.get("/personas", response_model=List[PersonaResponse])
def list_personas():
    return obtener_personas()


@app.get("/personas/{persona_id}", response_model=PersonaResponse)
def get_persona(persona_id: str):
    persona = obtener_persona(persona_id)
    if not persona:
        raise HTTPException(status_code=404, detail="Persona no encontrada")
    return persona


@app.post("/personas", response_model=PersonaResponse, status_code=201)
def create_persona(persona: PersonaCreate):
    return crear_persona(persona)


@app.put("/personas/{persona_id}", response_model=PersonaResponse)
def update_persona(persona_id: str, persona: PersonaCreate):
    updated = actualizar_persona(persona_id, persona)
    if not updated:
        raise HTTPException(status_code=404, detail="Persona no encontrada")
    return updated


@app.delete("/personas/{persona_id}", status_code=204)
def delete_persona(persona_id: str):
    if not eliminar_persona(persona_id):
        raise HTTPException(status_code=404, detail="Persona no encontrada")


# Carreras endpoints
@app.get("/carreras", response_model=List[CarreraResponse])
def list_carreras():
    return obtener_carreras()


@app.get("/carreras/{carrera_id}", response_model=CarreraResponse)
def get_carrera(carrera_id: str):
    carrera = obtener_carrera(carrera_id)
    if not carrera:
        raise HTTPException(status_code=404, detail="Carrera no encontrada")
    return carrera


@app.post("/carreras", response_model=CarreraResponse, status_code=201)
def create_carrera(carrera: CarreraCreate):
    return crear_carrera(carrera)


# Habilidades endpoints
@app.get("/habilidades", response_model=List[HabilidadResponse])
def list_habilidades():
    return obtener_habilidades()


@app.get("/habilidades/{habilidad_id}", response_model=HabilidadResponse)
def get_habilidad(habilidad_id: str):
    habilidad = obtener_habilidad(habilidad_id)
    if not habilidad:
        raise HTTPException(status_code=404, detail="Habilidad no encontrada")
    return habilidad


@app.post("/habilidades", response_model=HabilidadResponse, status_code=201)
def create_habilidad(habilidad: HabilidadCreate):
    return crear_habilidad(habilidad)


# Compatibilidad endpoint
@app.get("/compatibilidad/{persona_id}", response_model=List[CompatibilidadResponse])
def get_compatibilidad(persona_id: str):
    persona = obtener_persona(persona_id)
    if not persona:
        raise HTTPException(status_code=404, detail="Persona no encontrada")
    return obtener_compatibilidad(persona_id)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.API_HOST, port=settings.API_PORT)