import json

from utils import generate_embeddings, call_spellbook_api


def ingest_data(vector_store_name, splits):
    embeddings = generate_embeddings(splits)
    document_items = [
        {
            "embedding": embedding,
            "text": split
        }
        for split, embedding in zip(splits, embeddings)
    ]

    payload = {"items": document_items}

    response = call_spellbook_api(endpoint="api/v1/vector-stores/" + vector_store_name + "/documents", payload=payload)

    print(json.dumps(response, indent=2))
