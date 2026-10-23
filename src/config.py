import dotenv

dotenv.load_dotenv()  # reads GROQ_API_KEY from .env

# If you get "model not found", copy a current model name from https://console.groq.com
CHAT_MODEL = "qwen/qwen3.8-27b"
EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"   # runs locally, free
RAW_DATA_DIR = "data/raw"
INDEX_DIR = "vectorstore"

# Defaults used by the API. Update these after tuning.
CHUNK_SIZE = 500
CHUNK_OVERLAP = 100
TOP_K = 5
PROMPT_VERSION = "v1"