"""Run with the API running (uvicorn or docker compose up).
Usage: python -m evaluation.latency"""
import json, statistics, time
import requests

API = "http://localhost:8000/ask"
questions = [q["question"] for q in json.load(open("data/eval/questions.json", encoding="utf-8"))]

requests.post(API, json={"question": "warm up"})  # first call loads the index; excluded

times = []
for q in questions:
    t = time.time()
    requests.post(API, json={"question": q}, timeout=60).raise_for_status()
    times.append(time.time() - t)
    time.sleep(2)  # pause between requests to stay within free-tier rate limits

times.sort()
print(f"Requests: {len(times)}")
print(f"Average: {statistics.mean(times):.2f}s")
print(f"Median:  {statistics.median(times):.2f}s")
print(f"p95:     {times[int(len(times) * 0.95) - 1]:.2f}s")