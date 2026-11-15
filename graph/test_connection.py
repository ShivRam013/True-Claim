from graph.neo4j_connection import (
    test_connection,
    close_connection
)

try:
    test_connection()
finally:
    close_connection()