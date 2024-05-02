import os
import requests

import cohere
# from openai import OpenAI


def generate_embeddings(texts: str):
    # embedding_res = OpenAI().embeddings.create(input=text, model="text-embedding-ada-002")
    # embedding = embedding_res.data[0].embedding
    co = cohere.Client(os.getenv('COHERE_API_KEY'))
    response = co.embed(texts=texts, input_type='classification', embedding_types=['float'], model='embed-multilingual-v3.0')
    embeddings = response.embeddings.float
    return embeddings


def call_spellbook_api(endpoint: str, payload: dict):
    spellbook_base_url = os.environ.get("SPELLBOOK_BASE_URL")
    spellbook_api_key = os.environ.get("SPELLBOOK_API_KEY")

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {spellbook_api_key}",
    }
    url = spellbook_base_url + endpoint if spellbook_base_url else endpoint
    response = requests.request("POST", url, json=payload, headers=headers)
    return response.json()


def format_page(page):
    # reference (modified version for Arabic): https://stackoverflow.com/questions/78200728/how-to-avoid-pymupdf-fitz-interpreting-large-gaps-between-words-as-a-newline-c
    page_content = ""
    words = page.get_text("words", sort=True)  # words sorted vertical, then horizontal
    if len(words) == 0:
        return True, page_content
    line = [words[0]]  # list of words in same line
    for w in words[1:]:
        w0 = line[-1]  # get previous word
        if abs(w0[3] - w[3]) <= 3:  # same line (approx. same bottom coord)
            line.append(w)
        else:  # new line starts
            line.sort(key=lambda w: w[0], reverse=True)  # sort words in line right-to-left
            # print text of line
            text = " ".join([w[4] for w in line])
            page_content += text + "\n"
            line = [w]  # init line list again
    # print last line
    text = " ".join([w[4] for w in line[::-1]])
    page_content += text + "\n"
    page_content += chr(12) + "\n"
    return False, page_content
