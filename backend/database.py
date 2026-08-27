from neo4j import GraphDatabase, Driver
from backend.config import settings
import logging

logger = logging.getLogger(__name__)

_driver: Driver | None = None
_driver_initialized: bool = False


def get_driver() -> Driver:
    global _driver, _driver_initialized
    if _driver is None:
        _driver = GraphDatabase.driver(
            settings.NEO4J_URI,
            auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD)
        )
        _driver_initialized = True
    return _driver


def verify_connection() -> bool:
    """Verify database connectivity. Returns True if connected, False otherwise."""
    global _driver, _driver_initialized
    if not _driver_initialized:
        get_driver()
    try:
        _driver.verify_connectivity()
        logger.info(f"Connected to Neo4j database: {settings.NEO4J_DATABASE}")
        return True
    except Exception as e:
        logger.warning(f"Neo4j connection failed: {e}")
        return False


def close_driver():
    global _driver, _driver_initialized
    if _driver:
        _driver.close()
        _driver = None
        _driver_initialized = False
        logger.info("Neo4j driver closed")


def get_session():
    driver = get_driver()
    return driver.session(database=settings.NEO4J_DATABASE)