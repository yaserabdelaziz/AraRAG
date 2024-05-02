from dataclasses import dataclass
from typing import Callable, List

from transformers import AutoTokenizer


@dataclass
class Tokenizer:
    chunk_overlap: int
    tokens_per_chunk: int
    decode: Callable[[List[int]], str]
    encode: Callable[[str], List[int]]


def split_text_on_tokens(text: str, tokenizer: Tokenizer) -> List[str]:
    """Split incoming text and return chunks using tokenizer."""
    splits: list[str] = []
    input_ids = tokenizer.encode(text)[1:]
    start_idx = 0
    cur_idx = min(start_idx + tokenizer.tokens_per_chunk, len(input_ids))
    chunk_ids = input_ids[start_idx:cur_idx]
    while start_idx < len(input_ids):
        splits.append(tokenizer.decode(chunk_ids))
        start_idx += tokenizer.tokens_per_chunk - tokenizer.chunk_overlap
        cur_idx = min(start_idx + tokenizer.tokens_per_chunk, len(input_ids))
        chunk_ids = input_ids[start_idx:cur_idx]
    return splits


tokenizer = AutoTokenizer.from_pretrained("CohereForAI/c4ai-command-r-v01")
tokenizer = Tokenizer(
    chunk_overlap=50,
    tokens_per_chunk=500,
    decode=tokenizer.decode,
    encode=tokenizer.encode,
)
