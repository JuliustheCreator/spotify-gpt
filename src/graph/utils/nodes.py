from connection.neo4j import Neo4jConnection

def create_node(conn, label, properties):
    """
    Create a node with a given label and properties.
    :param conn: Neo4jConnection object
    :param label: Label of the node (e.g., 'Song', 'Artist', etc.)
    :param properties: Dictionary of properties for the node (e.g., {'song_id': '1', 'name': 'Song A'})
    """
    properties_string = ', '.join([f"{key}: ${key}" for key in properties])
    query = f"CREATE (n:{label} {{{properties_string}}}) RETURN n"
    conn.query(query, parameters=properties)
