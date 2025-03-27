import json
import sqlite3 as db
import jsonschema as schema_validator

DATABASE_NAME = 'rbfs_romanian_cities.db'

# def get_node_neighbours(node: Node) -> list[int]:

# TODO: Make Node to have a reference to a Problem object
#  (so the name of the graph corresponding to the problem
#  can be accessed)
def get_heuristic(node_state: str, graph_name: str) -> int:
    """
    Returns the heuristic value of the node with state ``node_state``
    """

    try:
        with db.connect(DATABASE_NAME) as connection:
            cursor = connection.cursor()
            cursor.execute(
                "SELECT value ->> 'heuristicValue' AS heuristicValue "
                "FROM graphs, json_each(data, '$.heuristics') "
                "WHERE "
                    "value ->> 'nodeName' = ? "
                    "AND name = ?",
                (node_state, graph_name)
            )
            heuristic_value = cursor.fetchone()[0]
            return int(heuristic_value)

    except db.Error as error:
        raise error

def get_adjacency_list(node_state: str, graph_name: str) -> list[int]:
    """
    Returns the adjacency list of the node with state ``node_state``
    """

    try:
        with db.connect(DATABASE_NAME) as connection:
            cursor = connection.cursor()
            cursor.execute(
                "SELECT value ->> 'adjacencyRow' AS adjacencyRow "
                "FROM graphs, json_each(data, '$.adjacencyMatrix') "
                "WHERE "
                    "value ->> 'nodeName' = ? "
                    "AND name = ?",
                (node_state, graph_name)
            )
            adjacency_list = json.loads(cursor.fetchone()[0])
            return adjacency_list

    except db.Error as error:
        raise error

def get_node_list(graph_name: str) -> list[str]:
    """
    Returns the list of node names in the graph.
    This list is usually used as an ordering
    (to assign an index to each node in the graph).

    :param graph_name The name of the graph in the database.
    """

    try:
        with db.connect(DATABASE_NAME) as connection:
            cursor = connection.cursor()
            cursor.execute(
                "SELECT value ->> 'nodeName' AS nodeName "
                "FROM graphs, json_each(data, '$.adjacencyMatrix') "
                "WHERE "
                    "name = ?",
                (graph_name,)
            )
            adjacency_list = cursor.fetchall()
            adjacency_list = [tup[0] for tup in adjacency_list]
            return adjacency_list

    except db.Error as error:
        raise error

def insert_graph(data: str, name: str = None, ) -> None:
    """
    Insert a graph into the database.
    """

    # TODO: Remove absolute path
    schema = json.loads(
        open(r'../../assets/schema.json').read())

    try:
        schema_validator.validate(json.loads(data), schema)
    except schema_validator.ValidationError as error:
        print(f"Invalid JSON: {error.message}")
        print(f"Aborting database insertion.")
        return

    try:
        with db.connect(DATABASE_NAME) as connection:
            cursor = connection.cursor()
            cursor.execute("INSERT INTO graphs (name, data) VALUES (?, ?)", (name, data))
            connection.commit()

    except db.Error as error:
        print(f"Error occurred: {error}")
        print(f"Aborting database insertion.")
        return
