from graph.graph_operations import create_demo_graph
from graph.neo4j_connection import close_connection

try:
    create_demo_graph()

finally:
    close_connection()