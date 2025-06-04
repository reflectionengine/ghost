import os
import re
from pathlib import Path
from collections import Counter
from typing import List, Tuple, Dict


DOCS_PATH = Path(__file__).parent / "docs"
CHUNK_SIZE = 100  # approximate number of words per chunk


def _tokenize(text: str) -> List[str]:
    return re.findall(r"\b\w+\b", text.lower())


class VectorStore:
    def __init__(self):
        self.chunks: List[Tuple[str, List[str]]] = []  # (text, tokens)

    def add_document(self, text: str):
        tokens = _tokenize(text)
        # simple chunking by word count
        for i in range(0, len(tokens), CHUNK_SIZE):
            chunk_tokens = tokens[i : i + CHUNK_SIZE]
            chunk_text = " ".join(chunk_tokens)
            self.chunks.append((chunk_text, chunk_tokens))

    def search(self, query: str, k: int = 3) -> List[str]:
        query_tokens = set(_tokenize(query))
        scored: List[Tuple[float, str]] = []
        for text, tokens in self.chunks:
            if not tokens:
                continue
            intersection = query_tokens.intersection(tokens)
            union = query_tokens.union(tokens)
            score = len(intersection) / len(union) if union else 0
            scored.append((score, text))
        scored.sort(reverse=True, key=lambda x: x[0])
        return [t for _, t in scored[:k]]


def load_documents(path: Path = DOCS_PATH) -> VectorStore:
    vs = VectorStore()
    for file in path.glob("*.md"):
        with file.open() as f:
            vs.add_document(f.read())
    return vs


def generate_report(query: str, passages: List[str], reflection: bool = False) -> Dict[str, str]:
    joined = " ".join(passages)
    tokens = _tokenize(joined)
    summary = " ".join(tokens[:40]) + "..." if tokens else "No content"
    risks = [w for w in tokens if w.startswith("risk")]  # crude risk detection
    strategy = "Consider further investigation and mitigation steps."
    contradiction = "None detected"
    if reflection:
        strategy += " (Reflection mode: include adversarial thinking.)"
    return {
        "summary": summary,
        "risks": ", ".join(risks) or "None identified",
        "strategy": strategy,
        "contradiction": contradiction,
    }
