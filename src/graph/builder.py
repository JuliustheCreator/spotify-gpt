from connection.neo4j import Neo4jConnection
from utils.nodes import create_node
from utils.nodes import create_node
from utils.relationships import create_relationship
from utils.query import get_all_nodes, get_all_relationships
from config.settings import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD


def build_knowledge_graph():
    conn = Neo4jConnection(uri=NEO4J_URI, user=NEO4J_USER, pwd=NEO4J_PASSWORD)

    create_node(conn, "Song", {"song_id": "1", "name": "Song A", "duration_ms": 210000})
    create_node(conn, "Artist", {"artist_id": "1", "name": "Artist X"})
    create_node(conn, "Album", {"album_id": "1", "name": "Album 1", "release_date": "2020-05-01"})
    create_node(conn, "Genre", {"name": "Pop"})

    create_relationship(conn, "Song", "Artist", {"song_id": "1"}, {"artist_id": "1"}, "PERFORMED_BY")
    create_relationship(conn, "Song", "Album", {"song_id": "1"}, {"album_id": "1"}, "PART_OF_ALBUM")
    create_relationship(conn, "Song", "Genre", {"song_id": "1"}, {"name": "Pop"}, "HAS_GENRE")

    create_node(conn, "Feature", {"name": "Strong Bassline"})
    create_relationship(conn, "Song", "Feature", {"song_id": "1"}, {"name": "Strong Bassline"}, "HAS_FEATURE")

    print("Nodes in the DB:")
    get_all_nodes(conn)
    
    print("\nRelationships in the DB:")
    get_all_relationships(conn)

    conn.close()

if __name__ == "__main__":
    build_knowledge_graph()

