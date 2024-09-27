from connection.neo4j import Neo4jConnection

def get_all_nodes(conn):
    query = "MATCH (n) RETURN n LIMIT 25"
    results = conn.query(query)
    for record in results:
        print(record)

def get_all_relationships(conn):
    query = "MATCH (n1)-[r]->(n2) RETURN n1, r, n2 LIMIT 25"
    results = conn.query(query)
    for record in results:
        print(record)