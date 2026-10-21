from functools import lru_cache
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings # type: ignore
from src import config


@lru_cache(maxsize=1)
def get_embeddings():
    """Local embedding model. Downloads once (~90 MB), then runs offline on CPU."""
    return HuggingFaceEmbeddings(
        model_name=config.EMBED_MODEL,
        encode_kwargs={"normalize_embeddings": True},
    )


def make_llm():
    return ChatGroq(model=config.CHAT_MODEL, temperature=0, max_tokens=300, max_retries=3)


def text_of(msg):
    """Always return plain text, whether msg is a message object or a string."""
    content = getattr(msg, "content", msg)
    if isinstance(content, str):
        return content.strip()
    if isinstance(content, list):
        return "".join(p if isinstance(p, str) else p.get("text", "") for p in content).strip()
    return str(content).strip()