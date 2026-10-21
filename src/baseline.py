import re
from rank_bm25 import BM25Okapi
from src.ingest import load_docs, split_docs


def tokenize(text):
    return re.findall(r"\w+", text.lower())


class KeywordBaseline:
    """Classic keyword search (BM25) over the same chunks."""

    def __init__(self, k=4, chunk_size=800, chunk_overlap=100):
        self.chunks = split_docs(load_docs(), chunk_size, chunk_overlap)
        self.bm25 = BM25Okapi([tokenize(c.page_content) for c in self.chunks])
        self.k = k

    def retrieve(self, question):
        scores = self.bm25.get_scores(tokenize(question))
        top = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[: self.k]
        return [self.chunks[i] for i in top]