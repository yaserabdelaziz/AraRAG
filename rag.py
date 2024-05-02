import os

import cohere

from prompts import prompt
from ingest import ingest_data
from text_splitter import split_text_on_tokens, tokenizer
from utils import generate_embeddings, call_spellbook_api


class RAG:
    vector_store_name = os.environ.get("VECTOR_STORE_NAME")

    def ingest_text(self, text: str):
        ingest_data(self.vector_store_name, split_text_on_tokens(text, tokenizer))

    def __call__(self, message: str, stream=False):
        payload = {"queryEmbedding": generate_embeddings([str(message)])[0], "k": 10}
        response = call_spellbook_api(
            endpoint="api/v1/vector-stores/" + self.vector_store_name + "/similarity-search", payload=payload
        )
        print(response)

        docs = [item["text"] for item in response["data"]["items"]]

        co = cohere.Client(os.getenv('COHERE_API_KEY'))
        # print("Message: ", str(message))
        # response = co.rerank(model="rerank-multilingual-v3.0", query=str(message), documents=docs, top_n=10, return_documents=True)
        # print(response)
        # docs = [doc.document.text for doc in response.results if doc.relevance_score > 0.1]

        information = "\n\n".join(docs)
        print(information)

        answer = ""
        print(prompt.format(pdf_file_content=information, message=message))
        for event in co.chat_stream(
            model='command-r',
            message=prompt.format(pdf_file_content=information, message=message),
            temperature=0.0,
            chat_history=[],
            prompt_truncation='AUTO',
            connectors=[]
        ):
            if event.event_type == "text-generation":
                answer += event.text

                if stream:
                    yield answer
            elif event.event_type == "stream-end":
                break
        if not stream:
            yield answer
