import json
import src.utils.db_util as db
import jsonschema as schema_validator

# command:
# python main.py --insert graph.json "my_graph"

def insert_graph(json_path, graph_name: str):

    # ensure json respects schema
    json_str = json.loads(open(json_path).read())
    schema = json.loads(open(json_path).read())

    try:
        schema_validator.validate(json_str, schema)
    except schema_validator.ValidationError as exception:
        print(f"{type(exception).__name__}: {exception}")
        print(f"Aborting database insertion.")
        return

    # TODO: insert in database
