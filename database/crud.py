
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.conexion import get_driver, NEO4J_DATABASE



def obtener_personas():
    query = """
        MATCH (p:Persona)
        RETURN p.id AS id, p.nombre AS nombre, p.edad AS edad,
               p.nivel_educativo AS nivel_educativo, p.email AS email
        ORDER BY p.nombre
    """
    driver = get_driver()
    try:
        with driver.session(database=NEO4J_DATABASE) as session:
            result = session.run(query)
            return [dict(r) for r in result]
    finally:
        driver.close()


def obtener_carreras():
    query = """
        MATCH (c:Carrera)
        RETURN c.id AS id, c.nombre AS nombre, c.descripcion AS descripcion, c.facultad AS facultad
        ORDER BY c.nombre
    """
    driver = get_driver()
    try:
        with driver.session(database=NEO4J_DATABASE) as session:
            result = session.run(query)
            return [dict(r) for r in result]
    finally:
        driver.close()


def obtener_habilidades():
    query = """
        MATCH (h:Habilidad)
        RETURN h.id AS id, h.nombre AS nombre, h.categoria AS categoria
        ORDER BY h.categoria, h.nombre
    """
    driver = get_driver()
    try:
        with driver.session(database=NEO4J_DATABASE) as session:
            result = session.run(query)
            return [dict(r) for r in result]
    finally:
        driver.close()


# Calculo de compatibilidad 

def obtener_compatibilidad(persona_id: str):
    
    query = """
        MATCH (p:Persona {id: $personaId})-[:LE_GUSTA]->(h:Habilidad)
        WITH p, collect(h.id) AS habilidadesPersona

        MATCH (c:Carrera)-[:REQUIERE]->(hc:Habilidad)
        WITH p, habilidadesPersona, c, collect(hc.id) AS habilidadesCarrera

        WITH c, habilidadesCarrera,
             [x IN habilidadesCarrera WHERE x IN habilidadesPersona] AS interseccion

        RETURN c.nombre AS carrera,
               size(interseccion) AS coincidencias,
               size(habilidadesCarrera) AS totalRequeridas,
               round(100.0 * size(interseccion) / size(habilidadesCarrera), 2) AS compatibilidad
        ORDER BY compatibilidad DESC
    """
    driver = get_driver()
    try:
        with driver.session(database=NEO4J_DATABASE) as session:
            result = session.run(query, personaId=persona_id)
            return [dict(r) for r in result]
    finally:
        driver.close()



def crear_persona(persona_id, nombre, edad, nivel_educativo, email, habilidades_ids):

    query = """
        MERGE (p:Persona {id: $id})
        SET p.nombre = $nombre, p.edad = $edad,
            p.nivel_educativo = $nivel_educativo, p.email = $email
        WITH p
        UNWIND $habilidades AS hid
        MATCH (h:Habilidad {id: hid})
        MERGE (p)-[:LE_GUSTA]->(h)
    """
    driver = get_driver()
    try:
        with driver.session(database=NEO4J_DATABASE) as session:
            session.run(
                query,
                id=persona_id, nombre=nombre, edad=edad,
                nivel_educativo=nivel_educativo, email=email,
                habilidades=habilidades_ids,
            )
    finally:
        driver.close()


if __name__ == "__main__":

    #Prueba rapida
    
    resultados = obtener_compatibilidad("p1")
    for r in resultados:
        print(f"{r['carrera']}: {r['compatibilidad']}% "
              f"({r['coincidencias']}/{r['totalRequeridas']})")