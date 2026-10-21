import os
from langchain_community.document_loaders import DirectoryLoader, TextLoader # type: ignore
from langchain_text_splitters import RecursiveCharacterTextSplitter # type: ignore
from langchain_community.vectorstores import FAISS # type: ignore
from src import config
from src.llm import get_embeddings


def load_docs():
    loader = DirectoryLoader(config.RAW_DATA_DIR, glob="**/*.md",
                             loader_cls=TextLoader, loader_kwargs={"encoding": "utf-8"})
    docs = loader.load()
    for d in docs:  # keep only the file name, used for citations
        d.metadata["source"] = os.path.basename(d.metadata["source"])
    return docs


def split_docs(docs, chunk_size, chunk_overlap):
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return splitter.split_documents(docs)


def build_index(chunk_size=config.CHUNK_SIZE, chunk_overlap=config.CHUNK_OVERLAP,
                out_dir=config.INDEX_DIR):
    docs = load_docs()
    chunks = split_docs(docs, chunk_size, chunk_overlap)
    db = FAISS.from_documents(chunks, get_embeddings())
    db.save_local(out_dir)
    print(f"Indexed {len(docs)} docs -> {len(chunks)} chunks -> saved to {out_dir}")


if __name__ == "__main__":
    build_index()