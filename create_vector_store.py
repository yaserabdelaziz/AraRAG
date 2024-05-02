import json
import os

from dotenv import load_dotenv

load_dotenv(override=True)
from utils import call_spellbook_api


def main():
    vector_store_name = os.environ.get("VECTOR_STORE_NAME")

    payload = {"name": vector_store_name}

    response = call_spellbook_api(endpoint="api/v1/vector-stores", payload=payload)

    print(json.dumps(response, indent=2))


if __name__ == "__main__":
    main()
