from .querygpt import QueryGPT
import argparse
import json
import logging
import sys
from typing import Any, Dict


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    pydantic_ai_logger = logging.getLogger("pydantic_ai")
    pydantic_ai_logger.setLevel(logging.DEBUG)

    # Suppress Neo4j deprecation warnings
    neo4j_logger = logging.getLogger("neo4j.notifications")
    neo4j_logger.setLevel(logging.ERROR)

    handler = logging.StreamHandler(sys.stdout)
    pydantic_ai_logger.addHandler(handler)

    parser = argparse.ArgumentParser(description="Run the NL-to-SQL pipeline.")
    parser.add_argument(
        "query", type=str, help="Natural language query to convert to SQL."
    )
    args = parser.parse_args()
    pipeline = QueryGPT()
    result: Dict[str, Any] = pipeline.generate_query(args.query)

    if "error" in result:
        print(f"An error occurred: {result['error']}")
    else:
        print("--- SQL Query ---")
        print(result["sql_result"].sql)
        print("\n--- Explanation ---")
        print(result["sql_result"].explanation)
        print("\n--- Result Preview ---")
        print(json.dumps(result["query_result"], indent=2))


if __name__ == "__main__":
    main()
