from typing import Optional
import uuid
from neo4j import Session
from backend.database import get_session
from backend.models import (
    PersonaCreate, PersonaResponse,
    CarreraCreate, CarreraResponse,
    HabilidadCreate, HabilidadResponse,
    CompatibilidadResponse
)


def obtener_personas() -> list[PersonaResponse]:
    query = """
        MATCH (p:Persona)
        OPTIONAL MATCH (p)-[:LE_GUSTA]->(h:Habilidad)
        RETURN p.id AS id, p.nombre AS nombre, p.edad AS edad,
               p.nivel_educativo AS nivel_educativo, p.email AS email,
               collect(h.id) AS habilidades
        ORDER BY p.nombre
    """
    with get_session() as session:
        result = session.run(query)
        return [PersonaResponse(**dict(r)) for r in result]


def obtener_persona(persona_id: str) -> Optional[PersonaResponse]:
    query = """
        MATCH (p:Persona {id: $id})
        OPTIONAL MATCH (p)-[:LE_GUSTA]->(h:Habilidad)
        RETURN p.id AS id, p.nombre AS nombre, p.edad AS edad,
               p.nivel_educativo AS nivel_educativo, p.email AS email,
               collect(h.id) AS habilidades
    """
    with get_session() as session:
        result = session.run(query, id=persona_id)
        record = result.single()
        return PersonaResponse(**dict(record)) if record else None


def crear_persona(persona: PersonaCreate) -> PersonaResponse:
    # Auto-generar ID si no se proporciona
    persona_id = persona.id or f"p_{uuid.uuid4().hex[:8]}"
    query = """
        MERGE (p:Persona {id: $id})
        SET p.nombre = $nombre, p.edad = $edad,
            p.nivel_educativo = $nivel_educativo, p.email = $email
        WITH p
        UNWIND $habilidades AS hid
        MATCH (h:Habilidad {id: hid})
        MERGE (p)-[:LE_GUSTA]->(h)
        RETURN p.id AS id, p.nombre AS nombre, p.edad AS edad,
               p.nivel_educativo AS nivel_educativo, p.email AS email,
               $habilidades AS habilidades
        LIMIT 1
    """
    with get_session() as session:
        result = session.run(
            query,
            id=persona_id,
            nombre=persona.nombre,
            edad=persona.edad,
            nivel_educativo=persona.nivel_educativo.value,
            email=persona.email,
            habilidades=persona.habilidades_ids
        )
        record = result.single()
        return PersonaResponse(**dict(record))


def actualizar_persona(persona_id: str, persona: PersonaCreate) -> Optional[PersonaResponse]:
    query = """
        MATCH (p:Persona {id: $id})
        SET p.nombre = $nombre, p.edad = $edad,
            p.nivel_educativo = $nivel_educativo, p.email = $email
        WITH p
        OPTIONAL MATCH (p)-[r:LE_GUSTA]->()
        DELETE r
        WITH p
        UNWIND $habilidades AS hid
        MATCH (h:Habilidad {id: hid})
        MERGE (p)-[:LE_GUSTA]->(h)
        RETURN p.id AS id, p.nombre AS nombre, p.edad AS edad,
               p.nivel_educativo AS nivel_educativo, p.email AS email,
               $habilidades AS habilidades
    """
    with get_session() as session:
        result = session.run(
            query,
            id=persona_id,
            nombre=persona.nombre,
            edad=persona.edad,
            nivel_educativo=persona.nivel_educativo.value,
            email=persona.email,
            habilidades=persona.habilidades_ids
        )
        record = result.single()
        return PersonaResponse(**dict(record)) if record else None


def eliminar_persona(persona_id: str) -> bool:
    query = """
        MATCH (p:Persona {id: $id})
        DETACH DELETE p
    """
    with get_session() as session:
        result = session.run(query, id=persona_id)
        return result.consume().counters.nodes_deleted > 0


def obtener_carreras() -> list[CarreraResponse]:
    query = """
        MATCH (c:Carrera)
        OPTIONAL MATCH (c)-[:REQUIERE]->(h:Habilidad)
        RETURN c.id AS id, c.nombre AS nombre, c.descripcion AS descripcion,
               c.facultad AS facultad, collect(h.id) AS requiere
        ORDER BY c.nombre
    """
    with get_session() as session:
        result = session.run(query)
        return [CarreraResponse(**dict(r)) for r in result]


def obtener_carrera(carrera_id: str) -> Optional[CarreraResponse]:
    query = """
        MATCH (c:Carrera {id: $id})
        OPTIONAL MATCH (c)-[:REQUIERE]->(h:Habilidad)
        RETURN c.id AS id, c.nombre AS nombre, c.descripcion AS descripcion,
               c.facultad AS facultad, collect(h.id) AS requiere
    """
    with get_session() as session:
        result = session.run(query, id=carrera_id)
        record = result.single()
        return CarreraResponse(**dict(record)) if record else None


def crear_carrera(carrera: CarreraCreate) -> CarreraResponse:
    # Auto-generar ID si no se proporciona
    carrera_id = carrera.id or f"c_{uuid.uuid4().hex[:8]}"
    query = """
        MERGE (c:Carrera {id: $id})
        SET c.nombre = $nombre, c.descripcion = $descripcion, c.facultad = $facultad
        WITH c
        UNWIND $requiere AS hid
        MATCH (h:Habilidad {id: hid})
        MERGE (c)-[:REQUIERE]->(h)
        RETURN c.id AS id, c.nombre AS nombre, c.descripcion AS descripcion,
               c.facultad AS facultad, $requiere AS requiere
        LIMIT 1
    """
    with get_session() as session:
        result = session.run(
            query,
            id=carrera_id,
            nombre=carrera.nombre,
            descripcion=carrera.descripcion,
            facultad=carrera.facultad,
            requiere=carrera.requiere
        )
        record = result.single()
        return CarreraResponse(**dict(record))


def obtener_habilidades() -> list[HabilidadResponse]:
    query = """
        MATCH (h:Habilidad)
        WHERE h.id IS NOT NULL AND h.nombre IS NOT NULL AND h.categoria IS NOT NULL
        RETURN h.id AS id, h.nombre AS nombre, h.categoria AS categoria
        ORDER BY h.categoria, h.nombre
    """
    with get_session() as session:
        result = session.run(query)
        return [HabilidadResponse(**dict(r)) for r in result]


def obtener_habilidad(habilidad_id: str) -> Optional[HabilidadResponse]:
    query = """
        MATCH (h:Habilidad {id: $id})
        RETURN h.id AS id, h.nombre AS nombre, h.categoria AS categoria
    """
    with get_session() as session:
        result = session.run(query, id=habilidad_id)
        record = result.single()
        return HabilidadResponse(**dict(record)) if record else None


def crear_habilidad(habilidad: HabilidadCreate) -> HabilidadResponse:
    # Auto-generar ID si no se proporciona
    habilidad_id = habilidad.id or f"h_{uuid.uuid4().hex[:8]}"
    query = """
        MERGE (h:Habilidad {id: $id})
        SET h.nombre = $nombre, h.categoria = $categoria
        RETURN h.id AS id, h.nombre AS nombre, h.categoria AS categoria
    """
    with get_session() as session:
        result = session.run(
            query,
            id=habilidad_id,
            nombre=habilidad.nombre,
            categoria=habilidad.categoria.value
        )
        record = result.single()
        return HabilidadResponse(**dict(record))


def obtener_compatibilidad(persona_id: str) -> list[CompatibilidadResponse]:
    query = """
        MATCH (p:Persona {id: $personaId})-[:LE_GUSTA]->(h:Habilidad)
        WITH p, collect(h.id) AS habilidadesPersona

        MATCH (c:Carrera)-[:REQUIERE]->(hc:Habilidad)
        WITH p, habilidadesPersona, c, collect(hc.id) AS habilidadesCarrera

        WITH c, habilidadesCarrera,
             [x IN habilidadesCarrera WHERE x IN habilidadesPersona] AS interseccion

        RETURN c.nombre AS carrera,
               size(interseccion) AS coincidencias,
               size(habilidadesCarrera) AS total_requeridas,
               round(100.0 * size(interseccion) / size(habilidadesCarrera), 2) AS compatibilidad
        ORDER BY compatibilidad DESC
    """
    with get_session() as session:
        result = session.run(query, personaId=persona_id)
        return [CompatibilidadResponse(**dict(r)) for r in result]


def obtener_estadisticas() -> dict:
    queries = {
        "total_personas": "MATCH (p:Persona) RETURN count(p) AS total",
        "total_carreras": "MATCH (c:Carrera) RETURN count(c) AS total",
        "total_habilidades": "MATCH (h:Habilidad) RETURN count(h) AS total",
    }
    with get_session() as session:
        stats = {}
        for key, q in queries.items():
            result = session.run(q)
            stats[key] = result.single()["total"]
        return stats