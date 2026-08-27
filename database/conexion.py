

import os
from neo4j import GraphDatabase
from dotenv import load_dotenv

load_dotenv()

NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USER = os.getenv("NEO4J_USER")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
NEO4J_DATABASE = os.getenv("NEO4J_DATABASE", "neo4j")

def get_driver():
    
    if not all([NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD]):
        raise ValueError(
            "Faltan variables de entorno. Revisa que exista un archivo .env "
            "con NEO4J_URI, NEO4J_USER y NEO4J_PASSWORD."
        )
    return GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))


def verificar_conexion():
    driver = get_driver()
    try:
        driver.verify_connectivity()
        with driver.session(database=NEO4J_DATABASE) as session:
            session.run("RETURN 1")
        print(f"Conexion exitosa a Neo4j. Base de datos objetivo: '{NEO4J_DATABASE}'")
    finally:
        driver.close()

print("Conexion directa no importa dondee")
if __name__ == "__main__":
    verificar_conexion()
    print("Conexion directa solo si es DIRECTA")