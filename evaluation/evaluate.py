"""Compares BM25 baseline vs several RAG configurations on the 50 test questions.
Usage:  python -m evaluation.evaluate        (all 50 questions)
        python -m evaluation.evaluate 3      (quick test with 3 questions)

Every LLM response is cached in evaluation/llm_cache.json. If you hit a quota,
wait and run the same command again: it continues where it stopped.
"""
import csv, hashlib, json, os, re, sys, time
from src.ingest import build_index
from src.rag import BIAssistant, generate_answer
from src.baseline import KeywordBaseline
from src.llm import make_llm, text_of

MIN_SECONDS_BETWEEN_CALLS = 4     # raise this if you see many rate-limit messages
CACHE_FILE = "evaluation/llm_cache.json"

JUDGE_PROMPT = """You are grading an answer from a BI assistant.
Question: {question}
Reference answer: {reference}
Assistant answer: {answer}

Score from 1 to 5:
5 = fully correct and complete, 4 = mostly correct, 3 = partly correct,
2 = mostly wrong or vague, 1 = wrong, or says the information was not found.
Reply with only the number."""

EXPERIMENTS = [
    {"name": "bm25_baseline", "type": "bm25", "chunk_size": 800, "chunk_overlap": 100, "k": 4, "prompt": "v1"},
    {"name": "rag_v1", "type": "rag", "chunk_size": 1000, "chunk_overlap": 0,   "k": 3, "prompt": "v1"},
    {"name": "rag_v2", "type": "rag", "chunk_size": 800,  "chunk_overlap": 100, "k": 4, "prompt": "v1"},
    {"name": "rag_v3", "type": "rag", "chunk_size": 500,  "chunk_overlap": 100, "k": 5, "prompt": "v1"},
    {"name": "rag_v4", "type": "rag", "chunk_size": 500,  "chunk_overlap": 100, "k": 5, "prompt": "v2"},
    {"name": "rag_v5", "type": "rag", "chunk_size": 800,  "chunk_overlap": 100, "k": 4, "prompt": "v2"},
]


class CachedLLM:
    """Groq with a gentle rate limiter, automatic retry on 429, and an on-disk cache."""

    def __init__(self):
        self.llm = make_llm()
        self.last_call = 0.0
        os.makedirs("evaluation", exist_ok=True)
        self.cache = {}
        if os.path.exists(CACHE_FILE):
            self.cache = json.load(open(CACHE_FILE, encoding="utf-8"))

    def invoke(self, prompt):
        key = hashlib.md5(prompt.encode("utf-8")).hexdigest()
        if key in self.cache:
            return self.cache[key]
        for attempt in range(6):
            wait = MIN_SECONDS_BETWEEN_CALLS - (time.time() - self.last_call)
            if wait > 0:
                time.sleep(wait)
            try:
                text = text_of(self.llm.invoke(prompt))
                break
            except Exception as e:
                msg = str(e).lower()
                if "429" in msg or "rate" in msg:
                    print(f"\n  Rate limit hit, waiting 60s (attempt {attempt + 1}/6)...")
                    time.sleep(60)
                    continue
                raise
        else:
            raise RuntimeError("Still rate limited. The daily quota may be used up; rerun later.")
        self.last_call = time.time()
        if not text:
            raise RuntimeError("The model returned an empty answer.")
        self.cache[key] = text
        json.dump(self.cache, open(CACHE_FILE, "w", encoding="utf-8"))
        return text


llm = CachedLLM()


def judge(question, reference, answer):
    out = llm.invoke(JUDGE_PROMPT.format(question=question, reference=reference, answer=answer))
    m = re.search(r"[1-5]", out)
    return int(m.group()) if m else 1


def run(exp, questions):
    if exp["type"] == "bm25":
        retrieve = KeywordBaseline(exp["k"], exp["chunk_size"], exp["chunk_overlap"]).retrieve
    else:
        index_dir = f"vectorstore_exp/c{exp['chunk_size']}_o{exp['chunk_overlap']}"
        if not os.path.exists(index_dir):
            build_index(exp["chunk_size"], exp["chunk_overlap"], index_dir)
        retrieve = BIAssistant(index_dir, exp["k"], exp["prompt"]).retrieve

    hits, scores = 0, []
    for i, q in enumerate(questions, 1):
        docs = retrieve(q["question"])
        if any(d.metadata["source"] in q["expected_sources"] for d in docs):
            hits += 1
        answer = generate_answer(llm, q["question"], docs, exp["prompt"])
        scores.append(judge(q["question"], q["reference"], answer))
        print(f"    question {i}/{len(questions)} done", end="\r")
    n = len(questions)
    return round(hits / n, 3), round(sum(scores) / n, 3)


if __name__ == "__main__":
    questions = json.load(open("data/eval/questions.json", encoding="utf-8"))
    if len(sys.argv) > 1:
        questions = questions[: int(sys.argv[1])]
    rows = []
    try:
        for exp in EXPERIMENTS:
            print(f"Running {exp['name']} ...")
            hit, score = run(exp, questions)
            rows.append({**exp, "hit_rate": hit, "avg_score": score})
            print(f"\n  hit_rate={hit}  avg_score={score}")
    except Exception as e:
        print(f"\nStopped: {e}")
        print("Progress is saved. Wait a while, then run the same command again.")
        sys.exit(1)

    base = rows[0]["avg_score"]
    for r in rows:
        r["improvement_vs_baseline_pct"] = round((r["avg_score"] - base) / base * 100, 1)

    with open("evaluation/results.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)

    print("\nname            chunk overlap k  prompt hit_rate avg_score improvement%")
    for r in rows:
        print(f"{r['name']:<15} {r['chunk_size']:<5} {r['chunk_overlap']:<7} {r['k']:<2} {r['prompt']:<6} "
              f"{r['hit_rate']:<8} {r['avg_score']:<9} {r['improvement_vs_baseline_pct']}")