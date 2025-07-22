import json


# Read config.json for API key and model name
with open("config.json", "r") as f:
    config = json.load(f)

class Config:
    GEMINI_API_KEY = config.get("GOOGLE_API_KEY")
    MODEL = config.get("model_name")
    EMBEDDINGS = config.get("embeddings_model")
    PROMPT = config.get("prompt")
    LANGSMITH_TRACING = config.get("LANGSMITH_TRACING")
    LANGSMITH_API_KEY = config.get("LANGSMITH_API_KEY")
    LANGSMITH_PROJECT = config.get("LANGSMITH_PROJECT")
    CHUNK_SIZE = config.get("chunk_size")
    OVERLAP = config.get("chunk_size")
    VECTOR_DB_PATH = config.get("VECTOR_DB_PATH")
    SEARCHAPI_API_KEY = config.get("SEARCHAPI_API_KEY")
    CSE_ID = config.get("CSE_ID")
