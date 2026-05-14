import os
from elasticsearch import Elasticsearch, ApiError
from dotenv import load_dotenv

load_dotenv()

# CLEAN URL: Ensure no trailing slashes or extra paths
ELASTIC_URL = os.getenv("ELASTIC_URL", "http://localhost:9200")

es = Elasticsearch(
    ELASTIC_URL,
    api_key=os.getenv("ELASTIC_API_KEY"),
    verify_certs=False, # Often needed for local dev
    request_timeout=30
)

INDEX_NAME = "job-market-data"

def init_index():
    try:
        # Check if index exists - ignore_status prevents the 404 exception
        if not es.indices.exists(index=INDEX_NAME):
            print(f"Creating index: {INDEX_NAME}")
            es.indices.create(
                index=INDEX_NAME,
                mappings={
                    "properties": {
                        "url": {"type": "keyword"},
                        "title": {"type": "text"},
                        "content": {"type": "text"},
                        "timestamp": {"type": "date"}
                    }
                }
            )
            print("Index created successfully.")
        else:
            print(f"Index '{INDEX_NAME}' already exists.")
    except ApiError as e:
        # If it's a 400 (already exists) we can ignore it
        if e.status_code == 400:
            print(f"Index '{INDEX_NAME}' already exists (caught 400).")
        else:
            print(f"Elasticsearch API Error: {e}")
    except Exception as e:
        print(f"Unexpected error initializing index: {e}")

def index_document(url, title, content):
    """Sends a crawled document to Elasticsearch, ensuring index exists first."""
    # Safety check: Initialize index if it's missing
    init_index() 
    
    doc = {
        "url": url,
        "title": title,
        "content": content,
        "timestamp": "now"
    }
    
    try:
        return es.index(index=INDEX_NAME, document=doc)
    except Exception as e:
        print(f"Failed to index document: {e}")
        return None