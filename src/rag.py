import time
from langchain_community.vectorstores import FAISS
from src import config
from src.llm import get_embeddings, make_llm, text_of

NOT_FOUND_TEXT = "couldn't find this in the bi documentation"

PROMPTS = {
    # v1 = plain prompt
    "v1": """Answer the question using the context.

Context:
{context}

Question: {question}
Answer:""",
    # v2 = engineered prompt: grounded, cites names, says "not found"
    "v2": """You are an enterprise BI knowledge assistant.
Rules:
1. Answer ONLY from the context below. Never use outside knowledge.
2. Always state the exact KPI, report, or table name you are describing.
3. For KPIs, include the formula and source tables when they are relevant.
4. If the context does not contain the answer, reply exactly: "I couldn't find this in the BI documentation."
5. Be concise (maximum 4 sentences).

Context:
{context}

Question: {question}
Answer:""",
}


def format_context(docs):
    return "\n\n".join(f"[Source: {d.metadata['source']}]\n{d.page_content}" for d in docs)


def generate_answer(llm, question, docs, prompt_version):
    prompt = PROMPTS[prompt_version].format(context=format_context(docs), question=question)
    return text_of(llm.invoke(prompt))


class BIAssistant:
    def __init__(self, index_dir=config.INDEX_DIR, k=config.TOP_K,
                 prompt_version=config.PROMPT_VERSION):
        self.db = FAISS.load_local(index_dir, get_embeddings(),
                                   allow_dangerous_deserialization=True)
        self.k = k
        self.prompt_version = prompt_version
        self.llm = make_llm()

    def retrieve(self, question):
        return self.db.similarity_search(question, k=self.k)

    def ask(self, question):
        start = time.time()
        docs = self.retrieve(question)
        answer = generate_answer(self.llm, question, docs, self.prompt_version)
        if NOT_FOUND_TEXT in answer.lower().replace("’", "'"):
            sources = []
        else:
            sources = sorted({d.metadata["source"] for d in docs})
        return {"answer": answer, "sources": sources, "latency_s": round(time.time() - start, 2)}