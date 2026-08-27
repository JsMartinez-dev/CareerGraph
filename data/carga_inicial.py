"""
Script de carga inicial de datos para CareerGraph.
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.conexion import get_driver


HABILIDADES = [
    {"id": "h1", "nombre": "Pensamiento logico", "categoria": "Cognitiva"},
    {"id": "h2", "nombre": "Programacion", "categoria": "Tecnica"},
    {"id": "h3", "nombre": "Analisis matematico", "categoria": "Cognitiva"},
    {"id": "h4", "nombre": "Creatividad", "categoria": "Blanda"},
    {"id": "h5", "nombre": "Comunicacion oral", "categoria": "Blanda"},
    {"id": "h6", "nombre": "Comunicacion escrita", "categoria": "Blanda"},
    {"id": "h7", "nombre": "Trabajo en equipo", "categoria": "Blanda"},
    {"id": "h8", "nombre": "Empatia", "categoria": "Blanda"},
    {"id": "h9", "nombre": "Diseno visual", "categoria": "Tecnica"},
    {"id": "h10", "nombre": "Resolucion de problemas", "categoria": "Cognitiva"},
    {"id": "h11", "nombre": "Investigacion cientifica", "categoria": "Academica"},
    {"id": "h12", "nombre": "Liderazgo", "categoria": "Blanda"},
    {"id": "h13", "nombre": "Manejo de datos", "categoria": "Tecnica"},
    {"id": "h14", "nombre": "Habilidad manual/tecnica", "categoria": "Tecnica"},
    {"id": "h15", "nombre": "Pensamiento critico", "categoria": "Cognitiva"},
]

CARRERAS = [
    {
        "id": "c1", "nombre": "Ingenieria de Sistemas",
        "descripcion": "Diseno y desarrollo de software y sistemas de informacion",
        "facultad": "Ingenieria",
        "requiere": ["h1", "h2", "h10", "h3"],
    },
    {
        "id": "c2", "nombre": "Ingenieria Industrial",
        "descripcion": "Optimizacion de procesos y recursos productivos",
        "facultad": "Ingenieria",
        "requiere": ["h3", "h13", "h12", "h10"],
    },
    {
        "id": "c3", "nombre": "Psicologia",
        "descripcion": "Estudio del comportamiento y procesos mentales",
        "facultad": "Ciencias Sociales",
        "requiere": ["h8", "h5", "h11", "h15"],
    },
    {
        "id": "c4", "nombre": "Diseno Grafico",
        "descripcion": "Creacion de piezas visuales y comunicacion grafica",
        "facultad": "Artes",
        "requiere": ["h4", "h9", "h6"],
    },
    {
        "id": "c5", "nombre": "Medicina",
        "descripcion": "Diagnostico, tratamiento y prevencion de enfermedades",
        "facultad": "Ciencias de la Salud",
        "requiere": ["h11", "h15", "h8", "h10"],
    },
    {
        "id": "c6", "nombre": "Derecho",
        "descripcion": "Estudio y aplicacion de las normas juridicas",
        "facultad": "Ciencias Sociales",
        "requiere": ["h5", "h6", "h15"],
    },
    {
        "id": "c7", "nombre": "Administracion de Empresas",
        "descripcion": "Gestion de organizaciones y recursos",
        "facultad": "Ciencias Economicas",
        "requiere": ["h12", "h7", "h13"],
    },
    {
        "id": "c8", "nombre": "Comunicacion Social",
        "descripcion": "Produccion y gestion de contenidos y medios",
        "facultad": "Ciencias Sociales",
        "requiere": ["h5", "h6", "h4"],
    },
]

PERSONAS = [
    {
        "id": "p1", "nombre": "Camila Torres", "edad": 17,
        "nivel_educativo": "Bachillerato", "email": "camila.torres@example.com",
        "le_gusta": ["h1", "h2", "h10", "h13"],  # -> Ingenieria de Sistemas
    },
    {
        "id": "p2", "nombre": "Daniel Rojas", "edad": 18,
        "nivel_educativo": "Bachillerato", "email": "daniel.rojas@example.com",
        "le_gusta": ["h11", "h15", "h8", "h5"],  # -> Medicina
    },
    {
        "id": "p3", "nombre": "Valentina Perez", "edad": 17,
        "nivel_educativo": "Bachillerato", "email": "valentina.perez@example.com",
        "le_gusta": ["h8", "h5", "h15", "h7"],  # -> Psicologia
    },
    {
        "id": "p4", "nombre": "Andres Gomez", "edad": 19,
        "nivel_educativo": "Tecnico", "email": "andres.gomez@example.com",
        "le_gusta": ["h5", "h6", "h15", "h12"],  # -> Derecho
    },
    {
        "id": "p5", "nombre": "Laura Jimenez", "edad": 18,
        "nivel_educativo": "Bachillerato", "email": "laura.jimenez@example.com",
        "le_gusta": ["h5", "h6", "h4", "h9"],  # -> Comunicacion Social
    },
]



def crear_constraints(tx):
    tx.run("CREATE CONSTRAINT persona_id_unique IF NOT EXISTS FOR (p:Persona) REQUIRE p.id IS UNIQUE")
    tx.run("CREATE CONSTRAINT carrera_id_unique IF NOT EXISTS FOR (c:Carrera) REQUIRE c.id IS UNIQUE")
    tx.run("CREATE CONSTRAINT habilidad_id_unique IF NOT EXISTS FOR (h:Habilidad) REQUIRE h.id IS UNIQUE")


def crear_habilidades(tx, habilidades):
    tx.run(
        """
        UNWIND $habilidades AS h
        MERGE (n:Habilidad {id: h.id})
        SET n.nombre = h.nombre, n.categoria = h.categoria
        """,
        habilidades=habilidades,
    )


def crear_carreras(tx, carreras):
    tx.run(
        """
        UNWIND $carreras AS c
        MERGE (n:Carrera {id: c.id})
        SET n.nombre = c.nombre, n.descripcion = c.descripcion, n.facultad = c.facultad
        WITH n, c
        UNWIND c.requiere AS hid
        MATCH (h:Habilidad {id: hid})
        MERGE (n)-[:REQUIERE]->(h)
        """,
        carreras=carreras,
    )


def crear_personas(tx, personas):
    tx.run(
        """
        UNWIND $personas AS p
        MERGE (n:Persona {id: p.id})
        SET n.nombre = p.nombre, n.edad = p.edad,
            n.nivel_educativo = p.nivel_educativo, n.email = p.email
        WITH n, p
        UNWIND p.le_gusta AS hid
        MATCH (h:Habilidad {id: hid})
        MERGE (n)-[:LE_GUSTA]->(h)
        """,
        personas=personas,
    )


def main():
    driver = get_driver()
    try:
        with driver.session() as session:
            print("Creando constraints...")
            session.execute_write(crear_constraints)

            print("Cargando habilidades...")
            session.execute_write(crear_habilidades, HABILIDADES)

            print("Cargando carreras y relaciones REQUIERE...")
            session.execute_write(crear_carreras, CARRERAS)

            print("Cargando personas y relaciones LE_GUSTA...")
            session.execute_write(crear_personas, PERSONAS)

        print("Carga inicial completada con exito.")
    finally:
        driver.close()


if __name__ == "__main__":
    main()