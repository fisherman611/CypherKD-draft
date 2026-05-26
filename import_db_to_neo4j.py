# It's use only for Cypherbench
import argparse
import os
from dotenv import load_dotenv
from src.neo4j_connector import Neo4jConnector

load_dotenv()

GRAPH_NAMES = [
    "art",
    "biology",
    "company",
    "fictional_character",
    "flight_accident",
    "geography",
    "movie",
    "nba",
    "politics",
    "soccer",
    "terrorist_attack",
]


def parse_args():
    parser = argparse.ArgumentParser(description="Import Cypherbench graphs into Neo4j")
    parser.add_argument(
        "--graphs",
        nargs="+",
        default=["all"],
        help="Graphs to import (space-separated). Use 'all' to import everything.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing database data before import.",
    )
    parser.add_argument("--host", default="neo4j://127.0.0.1", help="Neo4j host URI.")
    parser.add_argument("--port", type=int, default=7687, help="Neo4j bolt port.")
    return parser.parse_args()


def resolve_graphs(graphs_arg):
    if len(graphs_arg) == 1 and graphs_arg[0].lower() == "all":
        return GRAPH_NAMES

    invalid = sorted(set(graphs_arg) - set(GRAPH_NAMES))
    if invalid:
        raise ValueError(
            f"Invalid graph(s): {', '.join(invalid)}. Valid values: {', '.join(GRAPH_NAMES)} or 'all'."
        )
    return graphs_arg


def main():
    args = parse_args()

    neo4j_password = os.getenv("NEO4J_PASSWORD")
    neo4j_username = os.getenv("NEO4J_USERNAME")

    if not neo4j_username or not neo4j_password:
        raise ValueError("Missing NEO4J_USERNAME or NEO4J_PASSWORD in environment variables.")

    selected_graphs = resolve_graphs(args.graphs)
    for graph_name in selected_graphs:
        db_name = graph_name.replace("_", ".")
        conn = Neo4jConnector(
            name="cypherbench-db",
            host=args.host,
            port=args.port,
            username=neo4j_username,
            password=neo4j_password,
            database=db_name,
        )
        print(f"Importing {graph_name} -> database {db_name}")
        conn.import_json_dataset(
            filepath=f"benchmarks/Cypherbench/graphs/simplekg/{graph_name}_simplekg.json",
            db_name=db_name,
            overwrite=args.overwrite,
        )


if __name__ == "__main__":
    main()

