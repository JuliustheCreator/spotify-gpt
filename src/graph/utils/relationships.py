from connection.neo4j import Neo4jConnection

def create_relationship(conn, label1, label2, node1_props, node2_props, relationship_type):
    """
    Create a relationship between two nodes.
    :param conn: Neo4jConnection object
    :param label1: Label of the first node (e.g., 'Song')
    :param label2: Label of the second node (e.g., 'Artist')
    :param node1_props: Properties to identify the first node (e.g., {'song_id': '1'})
    :param node2_props: Properties to identify the second node (e.g., {'artist_id': '1'})
    :param relationship_type: The type of relationship (e.g., 'PERFORMED_BY', 'HAS_FEATURE')
    """
    node1_string = ', '.join([f"{key}: ${key}_1" for key in node1_props])
    node2_string = ', '.join([f"{key}: ${key}_2" for key in node2_props])
    
    query = (f"MATCH (n1:{label1} {{{node1_string}}}) "
             f"MATCH (n2:{label2} {{{node2_string}}}) "
             f"MERGE (n1)-[:{relationship_type}]->(n2) "
             f"RETURN n1, n2")
    
    # Prepare parameters for both nodes
    parameters = {f"{key}_1": node1_props[key] for key in node1_props}
    parameters.update({f"{key}_2": node2_props[key] for key in node2_props})
    
    conn.query(query, parameters=parameters)
