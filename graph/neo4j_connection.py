import os
import certifi

from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()

# Use certifi's trusted CA bundle for SSL verification
os.environ["SSL_CERT_FILE"] = certifi.where()

URI = os.getenv("NEO4J_URI")
USERNAME = os.getenv("NEO4J_USERNAME")
PASSWORD = os.getenv("NEO4J_PASSWORD")

driver = GraphDatabase.driver(
    URI,
    auth=(USERNAME, PASSWORD)
)


def test_connection():
    driver.verify_connectivity()
    print("Successfully connected to Neo4j AuraDB!")


def close_connection():
    driver.close()